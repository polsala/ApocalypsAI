# nightly-disk-usage-alert

Utility that checks the root filesystem disk usage and alerts when it exceeds a configurable threshold. Useful for system administrators to add to cron jobs.

## Usage

```sh
./src/disk_usage_alert.sh [threshold]
```

- `threshold` (optional): percentage (0-100). Default is 80.

The script prints `OK: usage X%` if below threshold, otherwise `ALERT: usage X% exceeds threshold Y%` and exits with status 1.

## Example

```sh
./src/disk_usage_alert.sh 75
```

Add to cron:

```sh
0 * * * * /path/to/disk_usage_alert.sh 85 >> /var/log/disk_alert.log 2>&1
```
