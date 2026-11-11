# nightly-disk-usage-watcher

Utility that scans disk usage and warns when any filesystem exceeds a configurable usage threshold (default 80%). Handy for CI pipelines or cron jobs to preempt out‑of‑space issues.

## Usage

```sh
./src/disk-watcher.sh            # uses default 80% threshold
THRESHOLD=90 ./src/disk-watcher.sh   # custom threshold
```

The script respects the environment variable `DF_MOCK` for testing; if set, its value is used as the output of `df -P` instead of invoking the real command.

## Exit codes

- `0` – no filesystems exceed the threshold
- `1` – at least one filesystem exceeds the threshold
