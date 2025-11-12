# Log Anomaly Scanner

A vigilant utility designed to scan log files for user-defined regex patterns, acting as an early warning system for "anomalies" or critical events. Think of it as your personal digital sentinel, constantly sifting through the noise to find the whispers of impending digital doom (or just a misconfigured service).

## Features

*   **Pattern-based Scanning**: Define any number of regex patterns to search for.
*   **Directory Traversal**: Scans all files within a specified directory.
*   **Detailed Reporting**: Outputs filename, line number, matched content, and the pattern that triggered the alert.
*   **CLI Friendly**: Easy to integrate into CI/CD pipelines, cron jobs, or local development workflows.

## Installation

This utility is self-contained and requires no special installation beyond a Python 3.11+ environment.

1.  Navigate to the `utils/log-anomaly-scanner/` directory.
2.  Run the `scanner.py` script directly.

## Usage

```bash
python src/scanner.py <directory_path> -p <pattern1> [<pattern2> ...]
```

*   `<directory_path>`: The path to the directory containing the log files you want to scan.
*   `-p`, `--patterns`: One or more regex patterns to search for. These should be quoted if they contain spaces or special characters.

### Examples

**1. Scan for common error messages:**

```bash
python src/scanner.py /var/log/nginx -p "ERROR" "CRITICAL" "failed to connect"
```

This command will scan all files in `/var/log/nginx` for lines containing "ERROR", "CRITICAL", or "failed to connect".

**2. Scan for specific application-level warnings:**

```bash
python src/scanner.py ./app_logs -p "WARN: Deprecated API" "Authentication failed for user: \w+"
```

This will look for lines indicating deprecated API usage or specific authentication failures in the `app_logs` directory.

## Output

If anomalies are detected, the script will print a report to `stdout` and exit with status code `1`.
If no anomalies are found, it will print a success message and exit with status code `0`.

### Example Anomaly Report

```
Scanning './test_logs' for patterns: ['ERROR', 'WARN']

--- Anomaly Report ---

File: app.log
  Line 2 (Pattern: 'WARN'): WARN: Low disk space.
  Line 3 (Pattern: 'ERROR'): ERROR: Failed to connect.

File: web.log
  Line 5 (Pattern: 'ERROR'): ERROR: DB connection lost.

--- Scan Complete: Anomalies Found! ---
```

## Development

To run tests:

```bash
python -m unittest tests/test_scanner.py
```
