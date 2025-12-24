# nightly-apt-cache-cleaner

A tiny Bash utility for Debian/Ubuntu systems that cleans up the APT package cache (`/var/cache/apt/archives`).

## Features

- Delete `.deb` files older than a configurable number of days (default 30).
- Dry‑run mode (`-n`) to preview deletions without touching the filesystem.
- Override the cache directory via `--cache-dir` or the `APT_CACHE_DIR` environment variable (useful for testing).
- Zero external dependencies – pure Bash and standard Unix tools.

## Installation

Copy the script to a location in your `$PATH`, e.g.:

```bash
mkdir -p ~/.local/bin
cp src/clean_apt_cache.sh ~/.local/bin/apt-cache-cleaner
chmod +x ~/.local/bin/apt-cache-cleaner
```

## Usage

```bash
apt-cache-cleaner [-d DAYS] [-n] [--cache-dir DIR]
```

- `-d DAYS` – Delete packages older than **DAYS** (default 30).
- `-n` – Dry‑run; only prints what would be deleted.
- `--cache-dir DIR` – Use a custom cache directory instead of the default `/var/cache/apt/archives`.

### Examples

- Show what would be removed from the default cache older than 60 days:

  ```bash
  apt-cache-cleaner -d 60 -n
  ```

- Actually delete files older than 15 days:

  ```bash
  sudo apt-cache-cleaner -d 15
  ```

- Run against a test directory (useful for CI):

  ```bash
  export APT_CACHE_DIR=/tmp/mock-apt-cache
  apt-cache-cleaner -n
  ```

## Testing

The utility includes a Bash test suite under `tests/`. Run it with:

```bash
bash tests/test_clean_apt_cache.sh
```

The tests create a temporary mock cache, populate it with files of known ages, and verify both dry‑run and actual deletion behavior.
