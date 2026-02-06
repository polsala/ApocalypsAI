# Nightly Log Scrubber

The `nightly-log-scrubber` is a whimsical-yet-useful utility designed to help maintain digital hygiene by scanning log files for common patterns of sensitive data and redacting them. Think of it as a digital dustpan for those accidental data spills in your logs.

## Features

-   **Sensitive Data Redaction**: Identifies and replaces patterns like email addresses, IP addresses, generic API keys, and simple password assignments with `[REDACTED]`.
-   **File and Directory Scanning**: Can process a single log file or recursively scan all files within a specified directory.
-   **Dry Run Mode**: Allows you to preview what would be redacted without making any permanent changes to your files.
-   **Whimsical Naming**: Because even serious tasks can have a touch of fun.

## Usage

### Prerequisites

-   Bash (version 4.0 or higher recommended)
-   `grep`
-   `sed`
-   `find` (for directory scanning)

### Running the Scrubber

1.  **Make the script executable:**
    ```bash
    chmod +x src/main.sh
    ```

2.  **Process a single file:**
    ```bash
    ./src/main.sh /path/to/your/logfile.log
    ```

3.  **Process a directory (recursively scans all files within):**
    ```bash
    ./src/main.sh /path/to/your/log_directory
    ```

4.  **Dry Run Mode (recommended for initial checks):**
    To see what changes would be made without actually modifying the files, use the `--dry-run` flag:
    ```bash
    ./src/main.sh /path/to/your/logfile.log --dry-run
    ./src/main.sh /path/to/your/log_directory --dry-run
    ```
    In dry-run mode, the script will output the lines that *would* be redacted, showing the `[REDACTED]` placeholder.

### Redaction Patterns

The scrubber currently looks for the following patterns:

-   **Email Addresses**: `user@domain.com`
-   **IPv4 Addresses**: `192.168.1.1`
-   **Generic API Keys**: Patterns like `API_KEY=abcdef1234567890abcdef1234567890`
-   **Simple Password Assignments**: Patterns like `password=mysecretpassword`

**Note**: The regex patterns are designed to catch common occurrences but are not exhaustive. For highly sensitive environments, consider more robust and configurable redaction tools.

## Development & Testing

### Running Tests

To ensure the scrubber is working as expected, you can run the provided test suite:

```bash
chmod +x tests/test_main.sh
./tests/test_main.sh
```

The tests create temporary files and directories to simulate various scenarios, including files with and without sensitive data, and dry-run operations. They are designed to be deterministic and self-contained.
