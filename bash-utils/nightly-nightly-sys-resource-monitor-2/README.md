## nightly-sys-resource-monitor

A whimsical yet practical bash script designed to keep an eye on your system's vital signs. It monitors CPU, RAM, and disk usage, and will "whisper" alerts if any resource breaches predefined thresholds. Perfect for keeping your digital homestead from succumbing to resource overload.

### Features

*   Monitors CPU, RAM, and Disk usage.
*   Configurable thresholds for each resource.
*   Simple, human-readable output.
*   "Whisper" alerts for exceeding thresholds.

### Usage

1.  **Clone the repository** and navigate to the `bash-utils/nightly-sys-resource-monitor` directory.
2.  **Make the script executable**: `chmod +x src/monitor.sh`
3.  **Run the script**: `./src/monitor.sh`

### Configuration

The script uses environment variables for configuration. You can set these before running the script:

*   `CPU_THRESHOLD`: Percentage of CPU usage to trigger an alert (default: 80).
*   `RAM_THRESHOLD`: Percentage of RAM usage to trigger an alert (default: 85).
*   `DISK_THRESHOLD`: Percentage of disk usage to trigger an alert (default: 90).
*   `DISK_PARTITION`: The disk partition to monitor (default: `/`).

**Example**: 
```bash
export CPU_THRESHOLD=75
export RAM_THRESHOLD=80
./src/monitor.sh
```

### Testing

Automated tests are included to ensure the script functions as expected. Run them using `bash tests/test_monitor.sh`.

### Philosophy

This utility embodies the ApocalypsAI spirit of "anarchy with discipline." It's a simple bash script, but it's isolated, testable, and serves a clear purpose in maintaining system stability in a chaotic digital world.
