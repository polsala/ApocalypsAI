# Nightly Syslog Parser

A whimsical yet useful bash utility to parse and filter syslog messages. It allows users to specify patterns to search for and customize the output format.

## Usage

```bash
./nightly-syslog-parser.sh [OPTIONS] <log_file>
```

## Options

*   `-p, --pattern <regex>`: The regular expression pattern to search for in syslog messages.
*   `-o, --output-format <format>`: The output format string. Available placeholders:
    *   `%timestamp%`: The timestamp of the log message.
    *   `%hostname%`: The hostname where the log originated.
    *   `%process%`: The process name that generated the log.
    *   `%message%`: The actual log message.
    *   Default format is `[%timestamp%] %hostname% %process%: %message%`.
*   `-h, --help`: Display this help message.

## Examples

1.  **Find all "error" messages in `/var/log/syslog` and display them in the default format:**
    ```bash
    ./nightly-syslog-parser.sh -p "error" /var/log/syslog
    ```

2.  **Find all messages from "sshd" and display only the timestamp and message:**
    ```bash
    ./nightly-syslog-parser.sh -p "sshd" -o "%timestamp% %message%" /var/log/syslog
    ```

3.  **Find messages containing "failed login" and output them with just the process and message:**
    ```bash
    ./nightly-syslog-parser.sh -p "failed login" -o "%process%: %message%" /var/log/auth.log
    ```

## Testing

To run the tests, navigate to the `tests` directory and execute:

```bash
./run_tests.sh
```
