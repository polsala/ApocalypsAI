# Nightly Syslog Parser

A whimsical yet useful bash script designed to parse and filter system logs. It helps you quickly find important messages amidst the digital chatter of your system.

## Features

*   **Keyword Filtering**: Search for specific words or phrases within syslog entries.
*   **Pattern Matching**: Utilize regular expressions for more advanced log analysis.
*   **Timestamp Filtering**: Optionally filter logs within a specific time range.
*   **Output Control**: Redirect output to a file or display it directly.

## Usage

```bash
./nightly-syslog-parser.sh -k "error" -f /var/log/syslog
```

This command will search the `/var/log/syslog` file for lines containing the word "error" and print them to the console.

### Options

*   `-k <keyword>`: Search for a specific keyword (case-insensitive).
*   `-p <pattern>`: Search using a regular expression pattern.
*   `-f <logfile>`: The path to the syslog file to parse. Defaults to `/var/log/syslog`.
*   `-s <start_time>`: Filter logs from this start time (e.g., "YYYY-MM-DD HH:MM:SS").
*   `-e <end_time>`: Filter logs up to this end time (e.g., "YYYY-MM-DD HH:MM:SS").
*   `-o <output_file>`: Redirect the output to a specified file.
*   `-h`: Display this help message.

## Examples

1.  **Find all "warning" messages in `/var/log/messages`**: 
    ```bash
    ./nightly-syslog-parser.sh -k "warning" -f /var/log/messages
    ```

2.  **Find lines containing "failed login" or IP addresses starting with 192.168.1. in `/var/log/auth.log`**: 
    ```bash
    ./nightly-syslog-parser.sh -p "failed login|192\.168\.1\." -f /var/log/auth.log
    ```

3.  **Find all "critical" errors between 2023-10-27 08:00:00 and 2023-10-27 10:00:00 and save to a file**: 
    ```bash
    ./nightly-syslog-parser.sh -k "critical" -s "2023-10-27 08:00:00" -e "2023-10-27 10:00:00" -o critical_errors.log
    ```

## Dependencies

*   `grep` (standard Unix utility)
*   `date` (standard Unix utility)

## Testing

Run the tests using the `tests/run_tests.sh` script.
