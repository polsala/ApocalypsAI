# Apoc Log Scrubber

A whimsical yet practical bash utility designed to cleanse your log files of any potentially sensitive information, leaving behind a clean, redacted version. Perfect for post-apocalyptic data wrangling or just keeping your logs tidy.

## Features

*   **Pattern-based Redaction**: Uses regular expressions to identify and replace common sensitive data patterns (e.g., IP addresses, email addresses, API keys).
*   **Customizable Patterns**: Easily extendable to include your own specific redaction rules.
*   **Dry Run Mode**: Preview the changes without actually modifying the log file.
*   **Whimsical Output**: Adds a touch of apocalyptic flair to the process.

## Usage

```bash
./src/main.sh <input_log_file> [--dry-run]
```

*   `<input_log_file>`: The path to the log file you want to scrub.
*   `--dry-run`: (Optional) If provided, the script will print the scrubbed output to standard output without modifying the original file.

## Examples

**Scrub a log file and overwrite it:**
```bash
./src/main.sh /var/log/syslog
```

**Preview scrubbing without modifying the file:**
```bash
./src/main.sh /var/log/auth.log --dry-run
```

## Extending Redaction Rules

To add new redaction rules, edit the `REDACTION_PATTERNS` array in the `src/main.sh` script. Each element should be a bash associative array with `pattern` and `replacement` keys.

Example:

```bash
REDACTION_PATTERNS=(
    "(" "pattern" "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" "replacement" "XXX.XXX.XXX.XXX"
    "(" "pattern" "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" "replacement" "[REDACTED_EMAIL]"
    # Add your custom patterns here
    # "(" "pattern" "YOUR_REGEX_HERE" "replacement" "YOUR_REPLACEMENT_HERE"
)
```

## Testing

Run the tests using the provided `tests/test_main.sh` script.

```bash
./tests/test_main.sh
```
