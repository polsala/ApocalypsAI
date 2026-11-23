# nightly-disk-usage-watcher

Utility that checks the disk usage of the root filesystem and prints a whimsical warning if usage exceeds a configurable threshold. Ideal for cron jobs or quick manual checks.

## Usage

```sh
./src/disk_watcher.sh            # uses default threshold 80%
THRESHOLD=90 ./src/disk_watcher.sh   # custom threshold
```

## How it works

The script runs `df -h /` (or reads from a mock file when `DF_MOCK_FILE` is set, useful for testing) and parses the usage percentage. If the usage exceeds the threshold, it prints an ASCII warning sign and exits with code 1; otherwise it prints a happy message and exits with 0.

## Testing

Run the bundled test script:

```sh
bash tests/test_disk_watcher.sh
```
