# Whispers of the Void Log Analyzer

## "Listen closely, for the void has whispers..."

This utility, affectionately known as the "Whispers of the Void Log Analyzer," is designed to help you detect subtle anomalies lurking within your system's log files. Think of it as an early warning system for cosmic disturbances in your digital realm. It scans specified log files for predefined patterns or keywords that might indicate unusual activity, errors, or potential issues, reporting them with context.

## Features

*   **Anomaly Detection**: Scans log files for user-defined or default patterns.
*   **Contextual Reporting**: Shows the line number and the full line where an anomaly was found.
*   **Customizable Patterns**: Easily extendable with your own anomaly patterns via a simple configuration file.
*   **Lightweight & Self-Contained**: A single Python script with minimal dependencies.

## Installation

No installation necessary! Simply navigate to the `utils/whispers-of-the-void-log-analyzer/` directory and run the `analyzer.py` script directly.

## Usage

```bash
python src/analyzer.py --log-file <path_to_your_log_file> [--patterns-file <path_to_your_patterns_file>]
```

### Arguments:

*   `--log-file <path>`: **Required**. The path to the log file you wish to analyze.
*   `--patterns-file <path>`: **Optional**. The path to a custom patterns file. If not provided, a set of default patterns will be used.

### Example:

To scan `my_app.log` using default patterns:

```bash
bash
python src/analyzer.py --log-file /var/log/my_app.log
```

To scan `system.log` using custom patterns defined in `my_custom_patterns.txt`:

```bash
python src/analyzer.py --log-file /var/log/system.log --patterns-file config/my_custom_patterns.txt
```

## Anomaly Patterns

Anomaly patterns are simple regular expressions, one per line, in a plain text file. The `config/patterns.txt` file provides a good starting point.

### `config/patterns.txt` example:

```
# Default anomaly patterns for Whispers of the Void Log Analyzer
# Each line is treated as a case-insensitive regular expression.
# Lines starting with '#' are ignored.

ERROR
CRITICAL
FAIL(ED)?
DENIED
WARNING
exception
segfault
panic
```

Each line in the patterns file is treated as a case-insensitive regular expression. Lines starting with `#` are ignored as comments.

## Development

To run tests:

```bash
python -m unittest tests/test_analyzer.py
```
