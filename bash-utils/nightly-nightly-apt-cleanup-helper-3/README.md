# nightly-apt-cleanup-helper

A whimsical Bash utility that helps you clean up unnecessary APT packages on Debian/Ubuntu systems, with apocalyptic flair. It can list packages that would be auto‑removed and optionally purge them. Supports dry‑run mode.

## Features

- **--list** – Show which packages are candidates for removal.
- **--clean** – Actually purge the listed packages.
- **--dry-run** – Show the commands that would be run without touching the system.
- **--file <path>** – Provide a custom file containing package names (one per line). If omitted, the script looks for `apt-autoremove-list.txt` in the current directory.

## Usage

```sh
# List packages from a custom file
./cleanup.sh --list --file sample.txt

# Dry‑run a purge (no changes made)
./cleanup.sh --clean --dry-run --file sample.txt

# Actually purge (use with caution!)
sudo ./cleanup.sh --clean --file sample.txt
```

## Why the apocalypse theme?

Because even your disk deserves a dramatic ending before the world ends. Let the script be the harbinger of order in the chaos of leftover packages.

## License

MIT © ApocalypsAI
