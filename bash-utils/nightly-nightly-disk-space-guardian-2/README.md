# nightly-disk-space-guardian

A whimsical bash utility that watches your disk usage and gently nudges you when space runs low. It can also perform a quick cleanup of stale temporary files.

## Usage

```sh
./main.sh [-t PERCENT] [-c]
```

- `-t PERCENT` – usage threshold (default 80)
- `-c` – perform cleanup of temporary files older than 1 day when threshold is exceeded.

## Example

```sh
./main.sh -t 75 -c
```

Will warn if the root partition is above 75% used and delete old `/tmp` files.
