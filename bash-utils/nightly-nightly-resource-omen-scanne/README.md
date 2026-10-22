# Nightly Resource Omen Scanner

Monitors system resources (CPU, Memory, Disk) and issues whimsical "omens" if configurable thresholds are breached, hinting at impending system strain or digital disquiet.

## Description

In the desolate digital landscape, it's crucial to heed the subtle whispers of your infrastructure. The `Nightly Resource Omen Scanner` acts as your vigilant sentinel, observing the vital signs of your system. Should CPU, memory, or disk usage climb beyond predefined limits, it doesn't just report numbers; it conjures a unique, whimsical "omen" – a poetic warning from the void, indicating that your system might be under stress or that unseen forces are at play.

This utility is perfect for adding a touch of apocalyptic charm to your system monitoring, making alerts less mundane and more... prophetic.

## Usage

The script can be run directly. It accepts optional arguments for custom thresholds and a log file path.

```bash
./src/resource_omen_scanner.sh [CPU_THRESHOLD] [MEMORY_THRESHOLD] [DISK_THRESHOLD] [DISK_PATH] [LOG_FILE]
```

### Arguments:

*   `CPU_THRESHOLD`: (Optional) CPU usage percentage (0-100) above which a CPU omen is triggered. Default: `80`.
*   `MEMORY_THRESHOLD`: (Optional) Memory usage percentage (0-100) above which a memory omen is triggered. Default: `80`.
*   `DISK_THRESHOLD`: (Optional) Disk usage percentage (0-100) for `DISK_PATH` above which a disk omen is triggered. Default: `90`.
*   `DISK_PATH`: (Optional) The disk path to monitor. Default: `/`.
*   `LOG_FILE`: (Optional) Path to a file where the report will be appended. If not provided, output goes only to stdout.

### Examples:

1.  **Run with default thresholds:**
    ```bash
    ./src/resource_omen_scanner.sh
    ```

2.  **Run with custom CPU threshold (90%) and default for others:**
    ```bash
    ./src/resource_omen_scanner.sh 90
    ```

3.  **Run with custom CPU (75%), Memory (70%), Disk (85%) thresholds for `/var` and log to `omens.log`:**
    ```bash
    ./src/resource_omen_scanner.sh 75 70 85 /var /tmp/omens.log
    ```

## Output

The script prints a "Resource Omen Scan Report" to standard output, detailing current resource usage and any triggered omens. If a `LOG_FILE` is specified, this report is also appended to that file.

**Example Output (No Omen):**
```
Resource Omen Scan Report (2023-10-27 10:30:00):
  CPU Usage: 15% (Threshold: 80%)
  Memory Usage: 30% (Threshold: 80%)
  Disk Usage (/): 45% (Threshold: 90%)
  All systems nominal. The void slumbers... for now.
```

**Example Output (With Omen):**
```
Resource Omen Scan Report (2023-10-27 10:30:00):
  CPU Usage: 92% (Threshold: 80%)
  Memory Usage: 75% (Threshold: 80%)
  Disk Usage (/): 88% (Threshold: 90%)
  CPU OMEN: The CPU core hums with an unnatural fervor, a sign of impending digital maelstrom!
Report logged to /tmp/omens.log
```

## Installation

1.  Navigate to the `bash-utils/nightly-resource-omen-scanner` directory.
2.  Make the script executable:
    ```bash
    chmod +x src/resource_omen_scanner.sh
    ```
3.  (Optional) For system-wide use, you can symlink or copy it to a directory in your `PATH`, e.g.:
    ```bash
    sudo ln -s "$(pwd)/src/resource_omen_scanner.sh" /usr/local/bin/resource-omen-scanner
    ```

## Automation

You can integrate this script into your cron jobs for regular monitoring:

```cron
# Run every 15 minutes, log omens to a file
*/15 * * * * /path/to/bash-utils/nightly-resource-omen-scanner/src/resource_omen_scanner.sh 85 85 95 /var /var/log/resource_omens.log >> /dev/null 2>&1
```

The script exits with status `0` if no omens are triggered, and `1` if at least one omen is triggered. This allows for easy integration into other monitoring systems or CI/CD pipelines.
