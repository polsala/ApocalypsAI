# Nightly Syslog Parser

A whimsical yet useful bash utility to parse and filter system logs for specific keywords or patterns. Perfect for quickly sifting through the digital detritus of your system.

## Usage

```bash
./nightly-syslog-parser.sh <log_file> <keyword1> [keyword2 ...]
```

*   `<log_file>`: The path to the system log file you want to parse (e.g., `/var/log/syslog`, `/var/log/auth.log`).
*   `<keyword1> [keyword2 ...]` : One or more keywords to search for within the log file. The script will return lines containing ANY of the provided keywords.

## Examples

*   Search for "error" and "warning" in `/var/log/syslog`:
    ```bash
    ./nightly-syslog-parser.sh /var/log/syslog error warning
    ```

*   Search for "failed login" in `/var/log/auth.log`:
    ```bash
    ./nightly-syslog-parser.sh /var/log/auth.log "failed login"
    ```

## Features

*   Parses standard syslog formats.
*   Supports multiple keywords for flexible filtering.
*   Case-insensitive search by default.
*   Outputs matching lines with their original timestamps.

## Testing

This utility includes a set of deterministic tests that do not require actual log files. Run `make test` in the `tests/` directory to execute them.
