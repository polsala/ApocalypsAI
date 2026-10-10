# Nightly Syslog Filter CLI

A whimsical yet practical bash script designed to filter and process system log (syslog) messages based on user-defined patterns. This utility is perfect for system administrators, developers, or anyone who needs to quickly sift through log data for specific events or anomalies.

## Features

*   **Pattern Matching**: Filter logs using regular expressions.
*   **Timestamp Filtering**: Select logs within a specific time range.
*   **Severity Level Filtering**: Isolate messages by their severity (e.g., ERROR, WARNING, INFO).
*   **Customizable Output**: Control the format of the output logs.
*   **Self-Contained**: No external dependencies beyond standard bash utilities.

## Usage

```bash
./nightly-syslog-filter-cli.sh [OPTIONS]
```

### Options

*   `-p, --pattern <regex>`: Filter logs matching the given regular expression.
*   `-s, --severity <level>`: Filter logs by severity level (e.g., `emerg`, `alert`, `crit`, `err`, `warning`, `notice`, `info`, `debug`).
*   `-t, --time-range <start_time> <end_time>`: Filter logs within a specified time range. Times should be in `YYYY-MM-DD HH:MM:SS` format.
*   `-o, --output-format <format>`: Specify the output format. Default is `raw`. Supported formats: `raw`, `json`.
*   `-h, --help`: Display this help message.

### Examples

1.  **Find all error messages from the last hour:**
    ```bash
    START_TIME=$(date -d '1 hour ago' '+%Y-%m-%d %H:%M:%S')
    END_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    ./nightly-syslog-filter-cli.sh -s err -t "$START_TIME" "$END_TIME"
    ```

2.  **Filter for messages containing 'failed login' and output as JSON:**
    ```bash
    ./nightly-syslog-filter-cli.sh -p 'failed login' -o json
    ```

3.  **Show all warning or critical messages:**
    ```bash
    ./nightly-syslog-filter-cli.sh -s warning -s crit
    ```
    *(Note: Multiple severity flags will be OR-ed together)*

## Testing

This utility includes a set of unit tests that can be run using `bashunit`. Ensure you have `bashunit` installed (`bash -c "$(curl -fsSL https://raw.githubusercontent.com/bashunit/bashunit/main/install.sh)"`).

To run tests:

```bash
cd tests
./run_tests.sh
```
