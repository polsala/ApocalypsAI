# Nightly Syslog Parser

A whimsical yet useful bash utility to parse and filter system logs. It allows you to search for specific keywords within your system's syslog files and present the results in a clean, customizable format.

## Features

*   **Keyword Filtering**: Search for one or more keywords in log entries.
*   **Log File Specification**: Specify which log files to parse (defaults to common syslog locations).
*   **Customizable Output**: Control the format of the output, including timestamps and log levels.
*   **Error Handling**: Basic error handling for file access and invalid arguments.

## Usage

```bash
./nightly-syslog-parser.sh -k "error" -k "warning" -l /var/log/syslog /var/log/auth.log
```

This command will search for lines containing either "error" or "warning" in `/var/log/syslog` and `/var/log/auth.log`.

### Options

*   `-k <keyword>`: Specify a keyword to search for. Can be used multiple times.
*   `-l <logfile>`: Specify a log file to parse. Can be used multiple times. If not provided, defaults to `/var/log/syslog` and `/var/log/auth.log`.
*   `-f <format>`: Specify the output format. Options:
    *   `default`: Standard syslog format.
    *   `json`: Output as JSON objects.
    *   `brief`: Only show the timestamp and the log message.
*   `-h`: Display help message.

## Installation

1.  Save the script as `nightly-syslog-parser.sh`.
2.  Make it executable: `chmod +x nightly-syslog-parser.sh`.

## Testing

Run the tests using `bash tests/test_syslog_parser.sh`.
