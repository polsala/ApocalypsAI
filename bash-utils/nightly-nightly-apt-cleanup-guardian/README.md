# nightly-apt-cleanup-guardian

**Purpose**: Keep your system tidy by removing stale `.deb` files from the APT cache, while sprinkling a bit of apocalyptic flair.

## Features
- Scan the APT cache (default `/var/cache/apt/archives` or `$APT_CACHE_DIR` if set).
- Delete files older than a configurable number of days (`--keep-days`, default 30).
- Dry‑run mode (`--dry-run`) to preview deletions.
- Colorful, themed messages to make cleanup feel like a pre‑apocalypse ritual.

## Installation
```sh
curl -fsSL https://example.com/nightly-apt-cleanup-guardian.sh -o /usr/local/bin/apt-cleanup.sh
chmod +x /usr/local/bin/apt-cleanup.sh
```

## Usage
```sh
# Real cleanup, keep files newer than 45 days
apt-cleanup.sh --keep-days=45

# Preview what would be removed
apt-cleanup.sh --dry-run

# Use a custom cache directory (useful for testing)
APT_CACHE_DIR=/tmp/fake-apt-cache apt-cleanup.sh --dry-run
```

## Exit codes
- `0` – Success (or nothing to delete in dry‑run).
- `1` – Invalid arguments.
- `2` – Deletion error.

## License
MIT
