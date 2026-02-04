# nightly-apt-cache-cleaner

**Purpose**: Keep your APT package cache tidy by deleting old versions of cached `.deb` files while preserving the newest version of each package. Works in dry‑run mode by default, with an optional `-y` flag to actually delete files.

## Installation

1. Clone the repository or copy the `src/clean_apt_cache.sh` script into a directory in your `$PATH`.
2. Make it executable:
   ```bash
   chmod +x /path/to/clean_apt_cache.sh
   ```

## Usage

```bash
clean_apt_cache.sh [-y]
```

- `-y` – Perform the deletions (otherwise the script only prints what *would* be deleted).

The script respects the environment variable `APT_CACHE_DIR` to point at a custom cache location (useful for testing). If not set, it defaults to `/var/cache/apt/archives`.

## Example

```bash
# Dry‑run (default)
clean_apt_cache.sh
# Output might be:
# Would delete: /var/cache/apt/archives/foo_1.0_amd64.deb

# Actually delete old packages
clean_apt_cache.sh -y
```

## How it works

1. Scans the cache directory for `*.deb` files.
2. Parses each filename assuming the pattern `package_version_arch.deb`.
3. Determines the newest version per package using `dpkg --compare-versions`.
4. Deletes (or lists) any older files.

## Testing

Run the bundled tests with:
```bash
cd tests && bash test_clean_apt_cache.sh
```
All tests should pass on any POSIX‑compatible system.
