# nightly-disk-guardian

A whimsical Bash utility that monitors root filesystem disk usage and warns you with apocalyptic messages when usage exceeds a threshold.

## Usage

```sh
./src/disk-guardian.sh
```

You can also set `DISK_THRESHOLD` environment variable to change the warning level (default 80). For testing, set `MOCK_DF` to a custom `df` output.

## How it works

The script runs `df -h /` (or uses `MOCK_DF` if provided), parses the used percentage, and if it exceeds the threshold prints a random apocalypse‑themed warning.

## License

MIT
