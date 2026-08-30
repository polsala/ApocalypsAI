# Nightly Syslog Filter

A whimsical yet useful bash utility to filter and process syslog messages based on configurable patterns. This script helps you keep your logs tidy and highlights important events in the chaos of system messages.

## Philosophy

"Anarchy with discipline" — this script provides a simple, yet powerful, way to manage your logs without complex dependencies. It's designed to be run as a cron job or integrated into other monitoring systems.

## Usage

```bash
./src/syslog_filter.sh <config_file>
```

Where `<config_file>` is a path to a configuration file defining the filtering rules.

## Configuration File Format

The configuration file is a simple text file where each line represents a filtering rule. Lines starting with `#` are comments.

Each rule follows the format:

`LEVEL:PATTERN:ACTION`

*   **LEVEL**: The syslog level to match (e.g., `INFO`, `WARNING`, `ERROR`, `CRITICAL`, `DEBUG`). If omitted, all levels are considered.
*   **PATTERN**: A regular expression to match against the syslog message content.
*   **ACTION**: What to do with the matched message. Supported actions:
    *   `LOG`: Print the message to standard output (default if omitted).
    *   `DROP`: Discard the message.
    *   `ALERT`: Print the message and send a simple alert (e.g., to stderr).

**Example Configuration (`config.txt`):**

```
# Ignore all debug messages
DEBUG:.*:DROP

# Alert on critical errors
CRITICAL:.*:ALERT

# Log all warnings
WARNING:.*:LOG

# Log specific kernel messages
:kernel:.*:LOG

# Drop noisy application messages
INFO:noisy_app:.*:DROP
```

## Examples

1.  **Basic Filtering**: Filter logs using `config.txt` and output to a file.
    ```bash
    ./src/syslog_filter.sh config.txt > filtered_logs.txt
    ```

2.  **Alerting Only**: Show only critical alerts.
    ```bash
    ./src/syslog_filter.sh config.txt | grep "ALERT:"
    ```

## Testing

This utility comes with a set of deterministic tests that do not require actual syslog access. You can run them using `bash`.

```bash
./tests/test_syslog_filter.sh
```
