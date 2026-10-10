A whimsical yet useful bash script to parse and filter system logs.

This utility allows you to sift through your system's syslog messages using customizable patterns, making it easier to find the information you need in the chaos of logs.

## Usage

```bash
./nightly-syslog-parser-cli.sh <log_file> <pattern>
```

*   `<log_file>`: The path to the syslog file you want to parse.
*   `<pattern>`: A grep-compatible pattern to filter the log entries.

## Examples

*   Find all entries related to 'sshd' in `/var/log/syslog`:
    ```bash
    ./nightly-syslog-parser-cli.sh /var/log/syslog "sshd"
    ```

*   Find all error messages (case-insensitive) in `/var/log/messages`:
    ```bash
    ./nightly-syslog-parser-cli.sh /var/log/messages "(?i)error"
    ```

## Testing

This utility includes a basic test suite to ensure its functionality.

To run the tests:

```bash
./nightly-syslog-parser-cli.sh --test
```

## Dependencies

*   `grep` (standard Unix utility)
*   `cat` (standard Unix utility)
