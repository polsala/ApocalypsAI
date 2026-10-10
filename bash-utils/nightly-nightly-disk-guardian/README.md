# nightly-disk-guardian

Utility that checks root filesystem disk usage and warns with apocalyptic messages if usage exceeds a threshold.

## Usage

```sh
./src/disk_guardian.sh [threshold]
```

If threshold omitted defaults to 80.

## How it works

- Reads `df -h /` (or uses `DF_OUTPUT` env var for testing)
- Parses usage percent.
- If usage > threshold, prints a random apocalypse-themed warning and exits with code 1.
- Otherwise exits 0.

## Testing

Run `bash tests/test_disk_guardian.sh`.
