# nightly-disk-emoji-report

Utility that reports disk usage of a given path with an emoji indicator.

## Usage

```sh
./src/disk-emoji-report.sh [path]
```

If no path is provided, the current directory is used.

The script prints:

```
Disk usage for <path>: <percent>% <emoji>
```

### Emoji meanings
- 🟢 0‑50%  (low usage)
- 🟡 51‑80% (moderate usage)
- 🔴 81‑100% (high usage)

## Tests

Run the test suite with:

```sh
bash tests/test_disk_emoji_report.sh
```
