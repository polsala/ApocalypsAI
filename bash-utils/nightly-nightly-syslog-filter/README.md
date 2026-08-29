## Nightly Syslog Filter

A whimsical yet useful bash utility to filter and process syslog messages based on configurable patterns. This script allows you to define patterns to include or exclude specific log entries, making it easier to manage and analyze your system logs.

### Features

*   **Pattern-based filtering**: Include or exclude log lines matching defined patterns.
*   **Configurable**: Easily modify patterns in the script itself.
*   **Timestamping**: Optionally add timestamps to filtered output.
*   **Self-contained**: A single bash script for ease of use.

### Usage

1.  **Save the script**: Save the following code as `nightly-syslog-filter.sh`.
2.  **Make it executable**: `chmod +x nightly-syslog-filter.sh`.
3.  **Run it**: Pipe your syslog data into the script, or redirect a log file.

    ```bash
    # Example: Filter /var/log/syslog for 'error' but exclude 'kernel panic'
    cat /var/log/syslog | ./nightly-syslog-filter.sh --include 'error' --exclude 'kernel panic'

    # Example: Filter a specific log file and add timestamps
    ./nightly-syslog-filter.sh --log-file /var/log/auth.log --include 'session opened' --timestamp
    ```

### Configuration

The script uses bash variables for configuration. You can modify these directly within the script:

*   `INCLUDE_PATTERNS`: An array of patterns to *include* in the output.
*   `EXCLUDE_PATTERNS`: An array of patterns to *exclude* from the output.
*   `ADD_TIMESTAMP`: Set to `true` to prepend a timestamp to each output line.

### Testing

Automated tests are included to verify the filtering logic. Run them using `bash tests/test_nightly-syslog-filter.sh`.
