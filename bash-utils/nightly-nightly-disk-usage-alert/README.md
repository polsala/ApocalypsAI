# nightly-disk-usage-alert

Utility that checks the disk usage of the root filesystem and alerts if it exceeds a configurable threshold. Useful for cron jobs or CI pipelines to prevent out‑of‑space failures.

## Usage

```sh
./src/disk_alert.sh            # uses default threshold 80%
THRESHOLD=90 ./src/disk_alert.sh   # custom threshold
```

The script can also be tested by providing a mock `df` output via the `DISK_USAGE_OUTPUT` environment variable:

```sh
DISK_USAGE_OUTPUT="$(cat tests/mock_df.txt)" ./src/disk_alert.sh
```

## Exit codes

- `0` – usage is below threshold
- `1` – usage is at or above threshold
- `2` – error (e.g., unable to parse)
