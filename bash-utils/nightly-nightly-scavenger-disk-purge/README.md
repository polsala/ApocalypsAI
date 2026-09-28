# nightly-scavenger-disk-purge

A whimsical bash utility that hunts down ancient log files and either archives them or removes them, helping keep your system tidy in the post‑apocalyptic wasteland.

## Usage

```sh
./scavenger.sh [-d DIR] [-a DAYS] [-n] [-c]
```

- `-d DIR` – directory to scan (default: /var/log)
- `-a DAYS` – age threshold in days (default: 7)
- `-n` – dry‑run; show what would be deleted/compressed without touching files
- `-c` – compress old files instead of deleting them

The script prints whimsical messages like “🗑️ Scavenging relics older than 7 days…”.

## Exit codes

- `0` – success
- `1` – error (e.g., invalid arguments or missing directory)
