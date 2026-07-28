# Nightly System Resource Monitor

A whimsical yet useful bash script to keep an eye on your system's vital signs. It monitors CPU, RAM, and Disk usage and can be configured to alert you when things get a bit too toasty.

## Features

*   **CPU Usage Monitoring**: Tracks overall CPU utilization.
*   **RAM Usage Monitoring**: Monitors memory consumption.
*   **Disk Usage Monitoring**: Checks free space on specified partitions.
*   **Configurable Thresholds**: Set your own limits for alerts.
*   **Simple Alerting**: Outputs messages to standard output when thresholds are breached.

## Usage

1.  **Clone the repository** and navigate to the `bash-utils/nightly-sys-resource-monitor` directory.
2.  **Make the script executable**: `chmod +x src/monitor.sh`
3.  **Configure thresholds**: Edit the `src/monitor.sh` file and adjust the `CPU_THRESHOLD`, `RAM_THRESHOLD`, and `DISK_THRESHOLD` variables.
4.  **Run the monitor**: `./src/monitor.sh`

## Example Configuration

```bash
# Set CPU usage threshold (percentage)
CPU_THRESHOLD=80

# Set RAM usage threshold (percentage)
RAM_THRESHOLD=85

# Set Disk usage threshold (percentage for root partition '/'). Add more partitions as needed.
DISK_THRESHOLD=90

# Disk partitions to monitor (space-separated)
MONITORED_DISKS="/"
```

## Testing

Run the provided tests using `bash tests/test_monitor.sh`.

## Contributing

Feel free to fork, improve, and submit pull requests! Let's keep our systems humming along happily.
