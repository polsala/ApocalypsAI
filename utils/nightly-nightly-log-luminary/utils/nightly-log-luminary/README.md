# Nightly Log Luminary

## Illuminate Your Logs

The Nightly Log Luminary is a simple, yet powerful Python utility designed to help you quickly scan and understand your log files. In the post-apocalyptic digital landscape, critical information can be buried under mountains of data. This tool acts as your personal beacon, highlighting errors, warnings, and providing a concise summary so you can focus on what truly matters.

## Features

*   **Log Parsing**: Reads any plain text log file.
*   **Severity Detection**: Identifies lines containing common log levels (ERROR, WARNING, CRITICAL, INFO, DEBUG) (case-insensitive).
*   **Summary Report**: Provides a count of each detected log level.
*   **Highlighted Output**: Optionally prints the log file with critical lines highlighted for easy visibility.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Installation

This utility is self-contained. Simply ensure you have Python 3.8+ installed.

## Usage

```bash
python src/luminary.py <log_file_path> [--highlight]
```

### Arguments:

*   `<log_file_path>`: The path to the log file you wish to analyze.
*   `--highlight`: (Optional) If present, the utility will print the entire log file with detected critical lines (ERROR, WARNING, CRITICAL) highlighted in red or yellow.

### Examples:

Analyze a log file and get a summary:

```bash
python src/luminary.py /var/log/syslog
```

Analyze a log file and see highlighted critical entries:

```bash
python src/luminary.py my_app.log --highlight
```

## Output Example

```
--- Log Luminary Report ---
File: my_app.log

Severity Summary:
  CRITICAL: 1
  ERROR   : 2
  WARNING : 3
  INFO    : 10
  DEBUG   : 5
  UNKNOWN : 2

Total Lines Scanned: 23

--- End Report ---

(If --highlight was used, the full log with highlights would follow)
```

## Development

To run tests:

```bash
python -m unittest tests/test_luminary.py
```
