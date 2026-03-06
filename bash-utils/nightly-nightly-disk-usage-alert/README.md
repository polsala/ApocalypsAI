# nightly-disk-usage-alert

Utility that scans disk usage and alerts when any filesystem exceeds a configurable threshold. Useful for cron jobs to preemptively warn about low disk space.

## Usage

```sh
./src/disk_alert.sh [threshold]
```

- `threshold` optional, default **80** (percent). Provide an integer.

The script prints lines like:

```
ALERT: /dev/sda1 at 92% usage
```

If no alerts are triggered, the script produces no output.

## Testing

Run the test suite with:

```sh
./tests/test_disk_alert.sh
```

The tests mock `df` output to ensure deterministic behavior.
