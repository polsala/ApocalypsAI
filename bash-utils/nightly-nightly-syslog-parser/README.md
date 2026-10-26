## Nightly Syslog Parser

This utility is a robust Bash script designed to parse and filter system log files. It allows users to search for specific keywords, IP addresses, or patterns within syslog entries, making it invaluable for system administrators and security analysts.

### Features

*   **Keyword Searching**: Find log entries containing specific words.
*   **Pattern Matching**: Utilize regular expressions for advanced pattern detection.
*   **IP Address Filtering**: Easily isolate logs related to particular IP addresses.
*   **Timestamp Filtering**: Optionally filter logs within a specified time range.
*   **Output Control**: Redirect filtered logs to stdout or a specified file.

### Usage

```bash
./nightly-syslog-parser.sh [-k "keyword"] [-p "pattern"] [-i <ip_address>] [-s <start_time>] [-e <end_time>] [-o <output_file>] [--help]
```

**Options**:

*   `-k "keyword"`: Search for log entries containing the specified keyword. Use quotes if the keyword contains spaces.
*   `-p "pattern"`: Search for log entries matching the given regular expression pattern.
*   `-i <ip_address>`: Filter logs by a specific IP address (IPv4 or IPv6).
*   `-s <start_time>`: Filter logs starting from this timestamp (e.g., "YYYY-MM-DD HH:MM:SS").
*   `-e <end_time>`: Filter logs up to this timestamp (e.g., "YYYY-MM-DD HH:MM:SS").
*   `-o <output_file>`: Write the filtered output to the specified file instead of stdout.
*   `--help`: Display this help message.

**Examples**:

1.  **Find all logs containing 'error'**: 
    ```bash
    ./nightly-syslog-parser.sh -k "error"
    ```

2.  **Find logs related to IP address 192.168.1.100**: 
    ```bash
    ./nightly-syslog-parser.sh -i 192.168.1.100
    ```

3.  **Find logs containing 'failed login' between two specific times**: 
    ```bash
    ./nightly-syslog-parser.sh -k "failed login" -s "2023-10-27 10:00:00" -e "2023-10-27 12:00:00"
    ```

4.  **Save logs matching a regex pattern to a file**: 
    ```bash
    ./nightly-syslog-parser.sh -p "^auth.*" -o auth_logs.txt
    ```

### Dependencies

*   `grep` (standard Unix utility)
*   `date` (standard Unix utility)
*   `awk` (standard Unix utility)

### Testing

Automated tests are included in the `tests/` directory. They use mock log files to ensure deterministic and offline execution.

To run tests:

```bash
cd tests
./run_tests.sh
```
