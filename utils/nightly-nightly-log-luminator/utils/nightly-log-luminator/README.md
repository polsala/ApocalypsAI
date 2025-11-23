# Nightly Log Luminator

## Overview
The Nightly Log Luminator is your trusty companion in the post-apocalyptic digital landscape, designed to shine a light on the dark corners of your log files. It scans specified directories for log files, identifies critical patterns (errors, warnings, custom keywords), and generates a concise summary report. No more sifting through mountains of text – let the Luminator guide your way!

## Features
- Scans directories recursively for log files.
- Supports multiple file extensions (e.g., `.log`, `.txt`).
- Identifies lines matching predefined keywords or regular expressions.
- Generates a summary report with counts and snippets of matched lines.

## Usage

```bash
python src/luminator.py --path /var/log --patterns "ERROR,WARNING,CRITICAL" --extensions "log,txt"
```

### Arguments
- `--path <directory>`: The root directory to start scanning for log files. (Required)
- `--patterns <comma-separated-patterns>`: A comma-separated list of keywords or regex patterns to search for. (Required)
- `--extensions <comma-separated-extensions>`: A comma-separated list of file extensions to consider as log files (e.g., `log,txt`). Defaults to `log`. (Optional)
- `--output <file_path>`: Path to save the report. If not provided, prints to console. (Optional)
- `--max-snippets <int>`: Maximum number of snippets to show per pattern per file. Defaults to 3. (Optional)

## Example Output

```
Luminator's Report - Scan Summary

Scanning directory: /var/log
Patterns searched: ERROR, WARNING, CRITICAL
File extensions: log, txt

---
File: /var/log/app.log
  Pattern 'ERROR': 2 matches
    - [Snippet 1] [Line 3] 2023-10-27 10:05:12 ERROR: Failed to connect to database.
    - [Snippet 2] [Line 5] 2023-10-27 10:15:30 ERROR: User authentication failed for 'admin'.
  Pattern 'WARNING': 1 match
    - [Snippet 1] [Line 2] 2023-10-27 10:00:05 WARNING: Disk space low on /data.

---
File: /var/log/auth.log
  Pattern 'CRITICAL': 1 match
    - [Snippet 1] [Line 6] 2023-10-27 09:30:00 CRITICAL: System reboot initiated by unknown process.

---
Total files scanned: 2
Total pattern matches found: 4
```

## Development
To run tests:
```bash
python -m unittest tests/test_luminator.py
```
