# Nightly Syslog Parser

A whimsical yet useful bash script designed to parse and filter system log messages (syslog). It allows users to search for specific keywords or patterns within log files, making it easier to diagnose issues or track events in a chaotic digital world.

## Features

*   **Keyword Search**: Filter logs based on one or more keywords.
*   **Pattern Matching**: Use regular expressions for more advanced filtering.
*   **Timestamp Filtering**: Optionally filter logs within a specific time range.
*   **Output Control**: Display matching lines or count occurrences.
*   **Customizable Log File**: Specify the syslog file to parse.

## Usage

```bash
./nightly-syslog-parser.sh -f /var/log/syslog -k "error" -p "kernel panic"
```

### Options

*   `-f <logfile>`: Path to the syslog file to parse. Defaults to `/var/log/syslog`.
*   `-k <keyword1,keyword2,...>`: Comma-separated list of keywords to search for. Case-insensitive.
*   `-p <pattern>`: A regular expression pattern to search for. Overrides keyword search if both are provided.
*   `-s <start_time>`: Start time for filtering (e.g., "2023-10-27 10:00:00"). Requires `date` command support.
*   `-e <end_time>`: End time for filtering (e.g., "2023-10-27 11:00:00"). Requires `date` command support.
*   `-c`: Count the number of matching log entries instead of displaying them.
*   `-h`: Display this help message.

## Examples

1.  **Find all 'error' messages in the default syslog file:**
    ```bash
    ./nightly-syslog-parser.sh -k "error"
    ```

2.  **Find lines containing 'segfault' or 'oom-killer' in a specific log file:**
    ```bash
    ./nightly-syslog-parser.sh -f /var/log/messages -k "segfault,oom-killer"
    ```

3.  **Find log entries matching a complex pattern (e.g., specific process ID):**
    ```bash
    ./nightly-syslog-parser.sh -p "process \[12345\]"
    ```

4.  **Count all 'warning' messages within a specific hour:**
    ```bash
    ./nightly-syslog-parser.sh -k "warning" -s "$(date -d '1 hour ago' '+%Y-%m-%d %H:%M:%S')" -e "$(date '+%Y-%m-%d %H:%M:%S')" -c
    ```

## Testing

Automated tests are included in the `tests/` directory. They use mock log files to ensure deterministic and offline execution.

To run tests:

```bash
cd tests
./run_tests.sh
```
