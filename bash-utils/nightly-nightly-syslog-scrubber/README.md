# Nightly Syslog Scrubber

A whimsical yet practical bash utility designed to keep your system logs clean and focused. This script acts as a filter for your syslog messages, removing common sensitive data and highlighting important events.

## Philosophy

"Anarchy with discipline" – this script embraces the freedom of bash for quick, effective system administration, while maintaining a disciplined approach to data sanitization and clarity.

## Features

*   **Sensitive Data Removal**: Strips out common patterns like IP addresses, usernames, and potentially sensitive keywords.
*   **Keyword Highlighting**: Emphasizes lines containing predefined critical keywords (e.g., "ERROR", "CRITICAL", "FAILURE").
*   **Timestamp Formatting**: Optionally reformats timestamps for better readability.
*   **Configurable**: Easily adjust filtering rules and keywords via environment variables or direct script modification.

## Usage

Pipe your syslog output to the script, or redirect a log file.

```bash
syslog-ng -F | ./nightly-syslog-scrubber.sh
cat /var/log/syslog | ./nightly-syslog-scrubber.sh
```

### Environment Variables

*   `SYSLOG_SCRUBBER_KEYWORDS`: A space-separated list of keywords to highlight (default: "ERROR CRITICAL FAILURE WARNING ALERT").
*   `SYSLOG_SCRUBBER_IP_MASK`: The string to replace IP addresses with (default: `[IP_REDACTED]`).
*   `SYSLOG_SCRUBBER_USER_MASK`: The string to replace usernames with (default: `[USER_REDACTED]`).
*   `SYSLOG_SCRUBBER_TIMESTAMP_FORMAT`: If set, attempts to reformat timestamps. Example: `+%Y-%m-%d %H:%M:%S`.

## Installation

1.  Save the script as `nightly-syslog-scrubber.sh`.
2.  Make it executable: `chmod +x nightly-syslog-scrubber.sh`.

## Testing

Run the provided test suite:

```bash
./run_tests.sh
```
