# Nightly System Resource Monitor

This utility is a simple yet effective bash script designed to monitor key system resources such as CPU, memory, and disk usage. It provides a snapshot of current usage and can be configured to alert when thresholds are exceeded.

## Features

*   Monitors CPU, Memory, and Disk usage.
*   Configurable thresholds for alerts.
*   Outputs a human-readable summary.
*   Designed for use in automated nightly checks.

## Usage

1.  **Save the script**: Save the `monitor_resources.sh` file to a desired location (e.g., `/usr/local/bin/monitor_resources.sh`).
2.  **Make it executable**: `chmod +x /usr/local/bin/monitor_resources.sh`
3.  **Run the script**: `./monitor_resources.sh`

### Configuration

The script uses environment variables for configuration. You can set these before running the script or modify the script directly.

*   `CPU_THRESHOLD`: The percentage of CPU usage above which an alert will be triggered (default: 80).
*   `MEM_THRESHOLD`: The percentage of memory usage above which an alert will be triggered (default: 80).
*   `DISK_THRESHOLD`: The percentage of disk usage above which an alert will be triggered (default: 90).
*   `ALERT_EMAIL`: An email address to send alerts to (if `sendmail` is configured).

**Example**: 
```bash
export CPU_THRESHOLD=90
export MEM_THRESHOLD=85
export ALERT_EMAIL="admin@example.com"
/usr/local/bin/monitor_resources.sh
```

## Testing

Automated tests are included to verify the script's functionality under different scenarios.

To run the tests:

1.  Navigate to the `tests` directory.
2.  Execute the test script: `bash test_monitor_resources.sh`

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
