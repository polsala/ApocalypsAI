# Nightly Chrono-Sync Beacon

## Summary
The `nightly-chrono-sync-beacon` is a whimsical-yet-useful bash utility designed to maintain temporal stability on your system. It periodically queries a designated NTP (Network Time Protocol) server to detect any 'temporal anomalies' (significant time drift) and can optionally synchronize your system's clock to ensure cosmic alignment.

## Features
- **Temporal Drift Detection**: Compares local system time with a reliable NTP source.
- **Anomaly Logging**: Logs any detected time deviations exceeding a configurable threshold.
- **Optional Synchronization**: Can automatically correct system time if a significant drift is found (requires `sudo` privileges for `sntp`).
- **Configurable**: Easy to adjust NTP server and drift threshold.

## Usage

### Prerequisites
- `bash` (most Linux/macOS systems have this)
- `sntp` command (part of `ntp` or `ntpsec` packages, or `ntpdate` on older systems). On Debian/Ubuntu: `sudo apt install ntpdate` or `sudo apt install ntpsec-ntpclient`.
- `bc` for floating-point comparisons (usually pre-installed, or `sudo apt install bc`).

### Running the Beacon
1. Make the script executable:
   ```bash
   chmod +x src/chrono_sync_beacon.sh
   ```
2. Run it directly:
   ```bash
   ./src/chrono_sync_beacon.sh
   ```

### Configuration
You can configure the beacon using environment variables:

- `NTP_SERVER`: The NTP server to query. Defaults to `pool.ntp.org`.
  Example: `NTP_SERVER="time.google.com" ./src/chrono_sync_beacon.sh`

- `DRIFT_THRESHOLD_SECONDS`: The maximum acceptable time difference in seconds before a 'temporal anomaly' is logged. Defaults to `5`.
  Example: `DRIFT_THRESHOLD_SECONDS="1.5" ./src/chrono_sync_beacon.sh`

- `SYNC_ENABLED`: Set to `true` to enable automatic time synchronization if a significant drift is detected. Defaults to `false`. **Note: Synchronization requires `sudo` privileges for the `sntp` command.**
  Example: `SYNC_ENABLED="true" sudo ./src/chrono_sync_beacon.sh`

- `LOG_FILE`: Path to the log file. Defaults to `/var/log/chrono_sync_beacon.log`. Output is also sent to `stdout`.
  Example: `LOG_FILE="/tmp/my_beacon.log" ./src/chrono_sync_beacon.sh`

### Example Cron Job (for daily checks)
To run the beacon daily and automatically synchronize if needed:

```cron
# Run the Chrono-Sync Beacon daily at 3:00 AM
0 3 * * * SYNC_ENABLED="true" /path/to/nightly-chrono-sync-beacon/src/chrono_sync_beacon.sh >> /var/log/chrono_sync_beacon_cron.log 2>&1
```

Remember to replace `/path/to/nightly-chrono-sync-beacon/` with the actual path to your utility.

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:
```bash
./tests/test_chrono_sync_beacon.sh
```

Tests are self-contained and use mocks to simulate `sntp` and `sudo` commands, ensuring deterministic and offline execution.
