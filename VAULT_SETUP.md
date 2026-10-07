# Obsidian setup

Keep images in `attachments/` inside this repository. Notes use standard Markdown
image links with paths relative to each note, so images work in Obsidian and GitHub.
Move or rename notes and images through Obsidian with automatic link updates enabled.

## Configure each computer

The current vault is the parent directory of this repository. Its `.obsidian/`
settings are outside the repository and do not sync through Obsidian Git.

After pulling this repository on another computer, close Obsidian and run from
the repository directory:

```sh
python3 scripts/configure_obsidian.py
```

On Windows, use `py scripts/configure_obsidian.py` if Python is installed through
the Python launcher. Then reopen Obsidian. The script preserves other settings
and configures:

| Setting | Value for the current vault layout |
| --- | --- |
| Use Wikilinks | Off |
| New link format | Path from current file |
| Automatically update internal links | On |
| Default location for new notes | In the folder specified below |
| Folder to create new notes in | `obsidian` |
| Default location for new attachments | In the folder specified below |
| Attachment folder path | `obsidian/attachments` |

These values can also be entered manually in Settings → Files and links.
If the repository itself is your vault, run
`python3 scripts/configure_obsidian.py --vault .` instead; the attachment path
will be `attachments` and new notes will be created at the vault root.

Let Git finish pulling before editing, and commit and push before switching
computers. Sync image files along with the notes that reference them.

## Missing older screenshots

Sixteen SQL screenshots referenced by the notes have not been uploaded. Put the
original files in `attachments/` with their existing `Pasted image … .png`
filenames; the links are already prepared for that location.
