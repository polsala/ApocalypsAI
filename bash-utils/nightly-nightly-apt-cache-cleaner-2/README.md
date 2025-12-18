# nightly-apt-cache-cleaner

Utility to identify and optionally purge old `.deb` packages from the APT cache, helping keep disk space tidy. Includes whimsical messages about the "wasteland of forgotten packages".

## Usage

```sh
./clean_apt_cache.sh [--days N] [--dry-run|--no-dry-run] [--cache-dir PATH]
```

### Options
- `--days N` : Consider files older than *N* days (default **30**).
- `--dry-run` : Only list files (default behavior).
- `--no-dry-run` : Actually delete the files.
- `--cache-dir PATH` : Path to the APT cache directory. If omitted, the script uses the environment variable `APT_CACHE_DIR` or falls back to `/var/cache/apt/archives`.

## Examples

```sh
# Dry‑run (default) – list packages older than 45 days
./clean_apt_cache.sh --days 45

# Actually delete old packages
./clean_apt_cache.sh --days 45 --no-dry-run

# Use a custom cache directory (useful for testing)
APT_CACHE_DIR=/tmp/mock-apt-cache ./clean_apt_cache.sh --dry-run
```

## Why?
In the post‑apocalyptic wasteland of your filesystem, old package files become debris. This script helps you clear the rubble before it overwhelms your storage.
