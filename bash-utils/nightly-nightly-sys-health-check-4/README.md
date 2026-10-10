## nightly-sys-health-check

A whimsical yet useful bash script to perform a quick system health check. It reports on disk usage, memory usage, and a summary of running processes.

### Usage

Run the script directly:

```bash
./nightly-sys-health-check.sh
```

### Output

The script will output a summary of the system's health, including:

*   **Disk Usage**: Shows the percentage of disk space used for the root partition.
*   **Memory Usage**: Displays the total, used, and free memory, along with the percentage used.
*   **Running Processes**: Lists the top 5 processes by CPU usage.

### Testing

Automated tests are included to ensure the script functions as expected. These tests mock the output of system commands to provide deterministic results.

To run the tests:

```bash
./tests/test_sys_health_check.sh
```
