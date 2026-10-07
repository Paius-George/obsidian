"""Configure this repository's containing Obsidian vault for portable images."""

import argparse
import json
from pathlib import Path


def main():
    repository = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault", type=Path, default=repository.parent,
        help="Vault directory (defaults to the repository's parent directory)",
    )
    args = parser.parse_args()
    vault = args.vault.resolve()
    try:
        repository_folder = repository.relative_to(vault)
    except ValueError:
        parser.error("The repository must be inside the chosen vault.")
    config_folder = vault / ".obsidian"
    if not config_folder.is_dir():
        parser.error("Open this directory as an Obsidian vault first, or pass --vault.")
    config_file = config_folder / "app.json"
    settings = json.loads(config_file.read_text()) if config_file.exists() else {}
    settings.update({
        "useMarkdownLinks": True,
        "newLinkFormat": "relative",
        "alwaysUpdateLinks": True,
        "attachmentFolderPath": (repository_folder / "attachments").as_posix(),
        "newFileLocation": "folder" if repository_folder.parts else "root",
        "newFileFolderPath": repository_folder.as_posix() if repository_folder.parts else "",
    })
    (repository / "attachments").mkdir(exist_ok=True)
    content = json.dumps(settings, indent=2) + "\n"
    if not config_file.exists() or config_file.read_text() != content:
        config_file.write_text(content)
    print(f"Configured {config_file}")
    print("Reopen Obsidian to load the settings.")


if __name__ == "__main__":
    main()
