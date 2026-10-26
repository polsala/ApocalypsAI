# Nightly Syslog Parser

A whimsical yet useful bash utility to parse and filter system logs.

This script allows you to quickly search through your system's syslog files for specific keywords, IP addresses, or patterns. It's designed to be run from the command line and provides flexible filtering options.

## Features

*   **Keyword Search**: Find lines containing specific words.
*   **IP Address Search**: Locate log entries associated with particular IP addresses.
*   **Pattern Matching**: Use regular expressions for advanced filtering.
*   **Log File Specification**: Specify which log file(s) to parse.
*   **Output Control**: Display matching lines or count them.

## Usage

```bash
./nightly-syslog-parser.sh -f /var/log/syslog -k "error" -i "192.168.1.100"
```

### Options

*   `-f <file>`: Path to the syslog file to parse. Can be specified multiple times for multiple files.
*   `-k <keyword>`: Search for lines containing this keyword (case-insensitive).
*   `-i <ip_address>`: Search for lines containing this IP address.
*   `-p <pattern>`: Search for lines matching this regular expression.
*   `-c`: Count the number of matching lines instead of displaying them.
*   `-h`: Display this help message.

## Examples

1.  **Find all "failed login" attempts in `/var/log/auth.log`:**
    ```bash
    ./nightly-syslog-parser.sh -f /var/log/auth.log -k "failed login"
    ```

2.  **Count occurrences of IP address `10.0.0.5` in `/var/log/messages`:**
    ```bash
    ./nightly-syslog-parser.sh -f /var/log/messages -i "10.0.0.5" -c
    ```

3.  **Find lines containing "warning" or "critical" using a regex in `/var/log/syslog`:**
    ```bash
    ./nightly-syslog-parser.sh -f /var/log/syslog -p "(warning|critical)"
    ```

## Installation

1.  Save the script as `nightly-syslog-parser.sh`.
2.  Make it executable: `chmod +x nightly-syslog-parser.sh`.

## Testing

Run the tests using the provided `test_nightly-syslog-parser.sh` script.

```bash
./tests/test_nightly-syslog-parser.sh
```
