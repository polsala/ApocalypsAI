# nightly-apt-cache-cleaner

A whimsical yet practical Bash utility that tidies up your APT package cache by removing
`.deb` files older than a configurable number of days. It supports a dry‑run mode so
you can preview what would be deleted before actually removing anything.

## Features
- **Age‑based cleanup** – keep only recent packages (default 30 days).
- **Dry‑run** (`-d`) to list candidates without deleting.
- **Custom cache location** – set `APT_CACHE_DIR` to point at a different directory
  (useful for testing).
- **Simple logging** – prints a concise summary of actions taken.

## Usage
```sh
./apt-cache-cleaner.sh [-d] [-n DAYS]
```

- `-d` Dry‑run mode (default is to actually delete).
- `-n DAYS` Number of days to retain packages (default 30).

## Example
```sh
# Show what would be removed, keeping the last 7 days of packages
APT_CACHE_DIR=/tmp/apt-cache ./apt-cache-cleaner.sh -d -n 7
```

## License
MIT
