## nightly-syslog-filter-sh

A whimsical yet practical bash script designed to filter and process system log messages (syslog). It allows users to define custom patterns to either include or exclude specific log entries, making log analysis more manageable.

### Philosophy

Inspired by the need to sift through the digital noise of system logs, this script aims to provide a simple, robust, and easily configurable tool for system administrators and developers. It embraces the 'anarchy with discipline' ethos by being a standalone, testable utility.

### Usage

1.  **Save the script**: Save the `syslog_filter.sh` file to a desired location (e.g., `/usr/local/bin/`).
2.  **Make it executable**: `chmod +x syslog_filter.sh`
3.  **Configure patterns**: Edit the `PATTERNS` variable within the script to define your inclusion and exclusion rules.
    *   Patterns are regular expressions.
    *   Lines matching an `INCLUDE_PATTERN` will be kept.
    *   Lines matching an `EXCLUDE_PATTERN` will be discarded, even if they match an `INCLUDE_PATTERN`.
    *   If `INCLUDE_PATTERN` is empty, all lines are considered for exclusion.
4.  **Run the script**: Pipe syslog output to the script, or provide a log file as an argument.

    *   **Pipe from syslog**: `tail -f /var/log/syslog | ./syslog_filter.sh`
    *   **Process a log file**: `./syslog_filter.sh /var/log/syslog`

### Configuration

*   `INCLUDE_PATTERNS`: An array of bash regular expressions. If any of these patterns match a log line, the line is considered for inclusion.
*   `EXCLUDE_PATTERNS`: An array of bash regular expressions. If any of these patterns match a log line, the line is excluded, overriding any inclusion.

### Example Configuration

```bash
# Include lines containing 'error' or 'warning', but exclude lines from 'systemd'
INCLUDE_PATTERNS=("error" "warning")
EXCLUDE_PATTERNS=("systemd")
```

### Testing

This utility comes with a set of deterministic tests that can be run using `bash` and `shunit2` (a common bash testing framework).

To run tests:

1.  Ensure you have `shunit2` installed or available in your PATH.
2.  Navigate to the `tests` directory.
3.  Run `bash test_syslog_filter.sh`.

### License

This utility is provided under the MIT License. See LICENSE for more details.
