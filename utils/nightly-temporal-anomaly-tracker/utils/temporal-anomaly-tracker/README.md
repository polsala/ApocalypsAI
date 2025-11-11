# Temporal Anomaly Tracker

Ever wonder if your system clock is secretly dabbling in time travel? The Temporal Anomaly Tracker is a whimsical-yet-critical utility designed to detect sudden, significant jumps in your system's time. Whether it's a mischievous NTP server, a VM snapshot revert, or a genuine temporal distortion, this tool will alert you to discrepancies that could wreak havoc on logs, scheduled tasks, and the very fabric of spacetime (or at least your application's sanity).

## Usage

Run `python src/anomaly_tracker.py` periodically (e.g., via cron). It will store its last observed time in a simple JSON file (`last_known_time.json` within its directory) and compare it on subsequent runs. 

```bash
# Example cron entry to run every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/your/repo/utils/temporal-anomaly-tracker/src/anomaly_tracker.py >> /var/log/temporal_anomaly.log 2>&1
```

## Configuration

Edit `src/anomaly_tracker.py` to adjust:

*   `THRESHOLD_SECONDS`: The maximum allowed time difference (in seconds) between runs before an anomaly is declared (default: 60 seconds).
*   `STATE_FILE`: The path to the JSON file where the last known timestamp is stored. By default, it's located next to the script.

## Output

If an anomaly is detected, the script will print a detailed alert message to standard output. Otherwise, it will confirm that the system time is stable.
