# Nightly Syslog Parser

A whimsical yet useful bash script designed to parse and filter system logs. It helps you quickly find relevant information within the often verbose output of system logs.

## Features

*   **Keyword Filtering**: Search for specific words or phrases.
*   **Pattern Matching**: Use regular expressions for advanced filtering.
*   **Timestamp Filtering**: Narrow down results by date and time ranges.
*   **Log Level Highlighting**: Optionally highlight different log levels (e.g., ERROR, WARNING).
*   **Customizable Output**: Control the format of the output.

## Usage

```bash
./nightly-syslog-parser.sh [OPTIONS] <log_file>
```

### Options

*   `-k, --keyword <keyword>`: Search for a specific keyword (case-insensitive).
*   `-p, --pattern <regex>`: Search using a regular expression.
*   `-s, --start-time <timestamp>`: Filter logs from this timestamp onwards (e.g., 'YYYY-MM-DD HH:MM:SS').
*   `-e, --end-time <timestamp>`: Filter logs up to this timestamp (e.g., 'YYYY-MM-DD HH:MM:SS').
*   `-l, --log-level <level>`: Highlight a specific log level (e.g., 'ERROR', 'WARN', 'INFO').
*   `-h, --help`: Display this help message.

### Examples

1.  **Find all 'error' messages in `/var/log/syslog`:**
    ```bash
    ./nightly-syslog-parser.sh -k error /var/log/syslog
    ```

2.  **Find lines containing 'failed login' using a regex:**
    ```bash
    ./nightly-syslog-parser.sh -p "failed login" /var/log/auth.log
    ```

3.  **Find messages between two specific times:**
    ```bash
    ./nightly-syslog-parser.sh -s "2023-10-27 10:00:00" -e "2023-10-27 11:00:00" /var/log/syslog
    ```

4.  **Highlight all 'WARNING' messages:**
    ```bash
    ./nightly-syslog-parser.sh -l WARN /var/log/messages
    ```

## Development Notes

This script uses standard bash utilities like `grep`, `awk`, and `date` for its functionality. It's designed to be run on most Linux/Unix-like systems.

## Testing

Automated tests are included in the `tests/` directory. They use mock log files to ensure deterministic and offline execution.
