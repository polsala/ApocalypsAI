# Nightly Log Scrubber

## Overview

The `Nightly Log Scrubber` is a crucial utility for any survivor in the data-rich, privacy-poor wasteland. It helps you sanitize your precious log files by redacting sensitive information like IP addresses, email addresses, and even custom patterns, ensuring your chronicles are safe for sharing without revealing too much to the wrong factions.

## Features

*   **IP Address Redaction**: Automatically replaces IPv4 addresses with `[REDACTED_IP]`. 
*   **Email Address Redaction**: Replaces email addresses with `[REDACTED_EMAIL]`. 
*   **Custom Pattern Redaction**: Allows users to define their own regular expressions to redact specific sensitive data.
*   **In-place or Output File**: Can either print to standard output or write to a specified output file.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond the standard library.

```bash
# No installation needed, just run the script directly.
```

## Usage

```bash
python3 src/scrubber.py --input <input_log_file> [--output <output_log_file>] [--custom-pattern <regex_pattern>] [--replacement <string>]
```

### Arguments

*   `--input <input_log_file>`: **Required**. Path to the log file to be scrubbed.
*   `--output <output_log_file>`: **Optional**. Path to the file where the scrubbed logs will be written. If not provided, output is printed to stdout.
*   `--custom-pattern <regex_pattern>`: **Optional**. A regular expression pattern to search for and redact. Can be specified multiple times for multiple patterns.
*   `--replacement <string>`: **Optional**. The string to replace custom-pattern matches with. Defaults to `[REDACTED_CUSTOM]`. This applies to *all* custom patterns.

### Examples

1.  **Scrubbing a log file and printing to console:**

    ```bash
    python3 src/scrubber.py --input my_server.log
    ```

2.  **Scrubbing and saving to a new file:**

    ```bash
    python3 src/scrubber.py --input access.log --output sanitized_access.log
    ```

3.  **Scrubbing with a custom pattern (e.g., credit card numbers):**

    ```bash
    python3 src/scrubber.py --input transactions.log --custom-pattern "\\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\\d{3})\\d{11})\\b" --replacement "[REDACTED_CC]"
    ```

4.  **Scrubbing with multiple custom patterns:**

    ```bash
    python3 src/scrubber.py --input audit.log \
        --custom-pattern "user_id=\\d+" \
        --custom-pattern "api_key=[a-zA-Z0-9]+" --replacement "[REDACTED_SENSITIVE]"
    ```

## Development

Contributions are welcome! Ensure tests pass and new features are covered by tests.
