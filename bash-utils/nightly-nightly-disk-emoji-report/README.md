# nightly-disk-emoji-report

Generates an emoji‑based disk usage summary for a given path.

## Usage

```sh
./disk_emoji_report.sh [path]
```

- If no path is provided, the current directory is used.
- The script prints a single line: `<emoji> <usage%> <mountpoint>`.

## Emoji mapping

- 🟢 0‑50 %  (low usage)
- 🟡 51‑80 % (moderate usage)
- 🔴 81‑100 % (high usage)

## Testing

The script respects the `MOCK_DF` environment variable. When set, its value is used instead of calling `df`. This enables deterministic testing.
