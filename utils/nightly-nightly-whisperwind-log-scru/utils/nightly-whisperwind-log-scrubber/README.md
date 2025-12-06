# Nightly Whisperwind Log Scrubber

## 🌬️ Silence the Whispers, Preserve the Truth 🌬️

The Nightly Whisperwind Log Scrubber is your trusty companion in the post-apocalyptic digital landscape, ensuring your precious log data can be shared and analyzed without revealing the secrets of the wasteland. It automatically detects and anonymizes common sensitive patterns, replacing them with generic, context-preserving placeholders.

### Features:

*   **IP Address Scrubbing**: Replaces IPv4 addresses with `[SCRUBBED_IP]`.
*   **Email Address Scrubbing**: Replaces email addresses with `[SCRUBBED_EMAIL]`.
*   **Generic Secret Scrubbing**: Identifies and replaces long alphanumeric strings (potential API keys, tokens, or sensitive IDs) with `[SCRUBBED_SECRET]`.
*   **Custom Pattern Support**: Allows you to define additional regular expressions for specific data you wish to anonymize.

### Usage:

To scrub a log file, run the `scrubber.py` script with your input and desired output file paths:

```bash
python src/scrubber.py <input_log_file> <output_scrubbed_file> [--patterns <regex1> <regex2> ...]
```

**Arguments:**

*   `<input_log_file>`: The path to the log file you want to scrub.
*   `<output_scrubbed_file>`: The path where the scrubbed log content will be saved.
*   `--patterns <regex1> <regex2> ...` (optional): One or more custom regular expressions to apply. Each pattern should be a valid Python regex string. Remember to quote patterns containing spaces or special characters.

### Examples:

1.  **Scrubbing a log file with default patterns:**
    ```bash
    python src/scrubber.py server.log scrubbed_server.log
    ```

2.  **Scrubbing and adding a custom pattern (e.g., specific user IDs like `user_ID_\d+`):**
    ```bash
    python src/scrubber.py app.log scrubbed_app.log --patterns "user_ID_\\d+"
    ```
    *(Note: Backslashes in regex patterns need to be escaped when passed as command-line arguments.)*

3.  **Scrubbing multiple custom patterns:**
    ```bash
    python src/scrubber.py debug.log clean_debug.log --patterns "transaction_\d{8}" "\bPIN:\s*\d{4}\b"
    ```

### Installation:

This utility is self-contained and requires Python 3.6+ (tested with 3.11). No external dependencies are needed beyond the standard library.

```bash
cd utils/nightly-whisperwind-log-scrubber
python src/scrubber.py --help
```
