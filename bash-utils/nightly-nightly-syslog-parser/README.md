# Nightly Syslog Parser

A whimsical yet useful bash script designed to parse and filter system log messages (syslog) for specific keywords or patterns. It's like a digital detective for your server's whispers!

## Features

*   **Keyword Filtering**: Easily search for specific words or phrases within syslog entries.
*   **Pattern Matching**: Utilize regular expressions for more advanced log analysis.
*   **Timestamp Filtering**: Filter logs based on date and time ranges.
*   **Output Control**: Redirect filtered logs to a file or display them on the console.
*   **Customizable**: Adapt the script to your specific logging needs.

## Usage

```bash
./nightly-syslog-parser.sh -k "ERROR" -t "2023-10-27 10:00:00" -e "2023-10-27 11:00:00" -o /var/log/filtered_errors.log
```

### Options

*   `-k <keyword>`: Search for a specific keyword (case-insensitive).
*   `-p <pattern>`: Search using a regular expression pattern.
*   `-t <start_time>`: Filter logs from this timestamp onwards (YYYY-MM-DD HH:MM:SS).
*   `-e <end_time>`: Filter logs up to this timestamp (YYYY-MM-DD HH:MM:SS).
*   `-f <log_file>`: Specify the syslog file to parse (defaults to `/var/log/syslog`).
*   `-o <output_file>`: Redirect output to a specified file.
*   `-h`: Display help message.

## Example Scenarios

*   **Find all "CRITICAL" errors in the last hour:**
    ```bash
    START_TIME=$(date -d '1 hour ago' '+%Y-%m-%d %H:%M:%S')
    ./nightly-syslog-parser.sh -k "CRITICAL" -t "$START_TIME"
    ```

*   **Find all messages related to "network" and save to a file:**
    ```bash
    ./nightly-syslog-parser.sh -p "network" -o network_activity.log
    ```

## Installation

1.  Save the script as `nightly-syslog-parser.sh`.
2.  Make it executable: `chmod +x nightly-syslog-parser.sh`.

## Testing

Run the provided test suite to ensure functionality:

```bash
./tests/run_tests.sh
```
