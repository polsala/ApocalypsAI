# Nightly Chronicle Keeper's Log Scrubber

## Overview

In the desolate future, information is power, but privacy is paramount. The "Chronicle Keeper's Log Scrubber" is a vital utility for maintaining the integrity and confidentiality of your precious log files. Whether you're safeguarding survivor manifests, resource inventories, or critical system diagnostics, this tool helps you anonymize sensitive data and filter out the noise, ensuring your chronicles are both clean and secure.

It's designed to be a simple, self-contained Python script that can be run from the command line.

## Features

*   **Sensitive Data Anonymization**: Automatically detects and replaces common sensitive patterns like IP addresses, email addresses, and credit card numbers with generic placeholders (e.g., `[ANONYMIZED_IP]`, `[REDACTED_EMAIL]`, `[HIDDEN_CARD]`).
*   **Keyword Filtering**: Filter log entries to include only lines containing specified keywords (case-insensitive).
*   **Flexible Output**: Writes processed logs to a new file, leaving your original data untouched.

## Usage

### Prerequisites

*   Python 3.6+ (tested with Python 3.11)

### Running the Scrubber

1.  Navigate to the `src` directory:
    ```bash
    cd utils/nightly-chronicle-keeper-log-scrubber/src
    ```
2.  Run the `scrubber.py` script with your desired options:

    ```bash
    python scrubber.py <input_file> <output_file> [--keywords KEYWORD [KEYWORD ...]] [--no-anonymize]
    ```

    **Arguments:**
    *   `<input_file>`: Path to the log file you want to scrub.
    *   `<output_file>`: Path where the scrubbed log will be saved.

    **Options:**
    *   `--keywords KEYWORD [KEYWORD ...]`: (Optional) Provide one or more keywords. Only lines containing any of these keywords will be included in the output. Keyword matching is case-insensitive.
    *   `--no-anonymize`: (Optional) Use this flag if you only want to filter logs by keywords and *not* anonymize any sensitive data. By default, anonymization is enabled.

### Examples

**1. Anonymize sensitive data in `server.log` and save to `scrubbed_server.log`:**

```bash
python scrubber.py ../../sample_logs/server.log scrubbed_server.log
```

**2. Filter `access.log` for "ERROR" or "WARNING" messages, and anonymize them:**

```bash
python scrubber.py ../../sample_logs/access.log filtered_errors.log --keywords ERROR WARNING
```

**3. Filter `debug.log` for "DEBUG" messages, but do NOT anonymize any data:**

```bash
python scrubber.py ../../sample_logs/debug.log debug_only.log --keywords DEBUG --no-anonymize
```

**4. Copy `journal.log` to `clean_journal.log` without anonymizing or filtering (effectively a copy):**

```bash
python scrubber.py ../../sample_logs/journal.log clean_journal.log --no-anonymize
```

## Development & Testing

To run the tests, navigate to the `tests` directory and use `unittest`:

```bash
cd utils/nightly-chronicle-keeper-log-scrubber/tests
python -m unittest test_scrubber.py
```

All tests are self-contained and deterministic, using `io.StringIO` and `unittest.mock` to simulate file operations without touching the filesystem.
