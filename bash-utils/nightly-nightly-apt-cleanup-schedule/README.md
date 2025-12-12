# nightly-apt-cleanup-scheduler

A whimsical Bash utility that scans the apt cache for old `.deb` packages, removes them, and prints a random apocalypse‑themed message.

## Usage

```sh
./src/cleanup.sh [days]
```

- `days` (optional): Age in days to consider a package old. Default is `30`.

The script requires `sudo` privileges to delete files.

## How it works

1. Finds `.deb` files older than the specified number of days in `/var/cache/apt/archives`.
2. Deletes them with `sudo rm -f`.
3. Prints a random message like “The caches crumble, but hope remains.”

## Testing

Run the test suite:

```sh
bash tests/test_cleanup.sh
```
