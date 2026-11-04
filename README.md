# SuiteCRM PoC bundle — 3 novel SQL injections (responsible-disclosure prep)

Target: SuiteCRM `hotfix` branch @ `ccb02b1e` (2026-10-29, post-7.15.2 line).
All three findings are **authenticated, quote-free SQL injections** — each is the
unpatched sibling of a sink SalesAgility already fixed in a nearby branch of the
same code. Each PoC script prints the exact requests it sends so you can replay
them in Burp Repeater; `burp-requests.md` has them pre-built.

| # | Script | Sink | Novel vs. |
|---|--------|------|-----------|
| 1 | `poc1_aor_conditions_field.py` | `AOR_Report.php:1591` — stored `aor_conditions.field` rendered raw | GHSA-4fhr-x4wr-fwqg fixed `aor_fields.field` only |
| 2 | `poc2_aor_date_param.py` | `AOR_Report.php:1717-1722` — request-driven `value_type=Date` params into `DATE_ADD()` | GHSA-239h-ffjr-v957 fixed `value_type=Field`; GHSA-pqq6-v2mj-hrm2 fixed `Multi` |
| 3 | `poc3_aow_date_condition.py` | `AOW_WorkFlow.php:590/609` — stored date-condition params into `DATE_ADD()`/`DATEADD()` | 2023 batch (CVE-2023-42632/33/34) hardened `$params[0]` only |

## Usage

```bash
python3 poc1_aor_conditions_field.py http://<host> <user> <password> --sleep 3
python3 poc2_aor_date_param.py       http://<host> <user> <password> --sleep 3
python3 poc3_aow_date_condition.py   http://<host> <user> <password> --sleep 3
```

Each script: logs in → saves the minimal report/workflow → triggers the query →
compares response times against a benign control → prints a verdict and the raw
requests for Burp. `--cleanup` marks the created records deleted. Exit code 0 = timing
delta observed.

Privilege needs: **all three** work for any non-admin user — #1/#2 need AOR Reports
access (create-your-own reports), #3 needs AOW_WorkFlow edit access (#2's *trigger*
needs only report view access). Non-admin reachability is what makes the CVSS
`PR:L` (8.8 / 6.5-8.8 / 6.8-8.8 depending on AOW ACL assignment).

## Environment

No instance was running on this machine when the PoCs were written — you need any
SuiteCRM ≥ 7.15 deployment (a stock 7.15.2/8.10.2 install is ideal for the advisory,
because the findings affect *currently patched* releases). Podman is available on
this machine; ask and a stack will be built (php-apache + mariadb + composer install
of the pinned commit).

## Notes

- Payloads need no quotes: SuiteCRM's global `securexss()` (include/utils.php,
  `clean_incoming_data()` at entryPoint) rewrites `'`→`&#039;` in every request
  value. Parens, spaces, letters and `--` survive — everything the payloads use.
- The MySQLi connector does not allow stacked queries, so time-based + UNION-read
  is the ceiling — consistent with how the sibling advisories (CVSS 8.8 C:H) were scored.
- `--sleep` controls `SLEEP(n)`; on table-scan plans MySQL may evaluate the subquery
  per row, so keep n small (3) and rely on the control-vs-payload delta, not absolute time.
