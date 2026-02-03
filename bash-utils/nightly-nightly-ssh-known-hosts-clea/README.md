# nightly-ssh-known-hosts-cleaner

**Purpose**: Keep your `~/.ssh/known_hosts` tidy by removing duplicate host entries.  The script can run in a *dry‑run* mode to show what would be removed without touching the file.

## Usage
```bash
./clean_known_hosts.sh [--dry-run] [path]
```
- `--dry-run` – prints the number of duplicate entries that *would* be removed, leaving the file untouched.
- `path` – optional path to the `known_hosts` file.  Defaults to `~/.ssh/known_hosts`.

## Examples
```bash
# Dry run on the default file
./clean_known_hosts.sh --dry-run

# Actually clean a custom file
./clean_known_hosts.sh /tmp/my_known_hosts
```

## How it works
The script reads the file, preserves the original order, and removes duplicate lines using an `awk` one‑liner.  It then either reports the number of duplicates (dry‑run) or overwrites the original file with the deduplicated version.

## Testing
Run the bundled test script:
```bash
cd tests && ./test_clean_known_hosts.sh
```
All tests should pass, confirming correct dry‑run output and proper removal of duplicates.
