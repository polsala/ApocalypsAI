# Nightly Data Debris Analyzer

## Overview

The Nightly Data Debris Analyzer is a whimsical yet practical utility designed to help you make sense of the digital 'debris' left behind in your log files. In the post-apocalyptic digital landscape, understanding the patterns in your system logs is crucial for survival. This tool sifts through specified log files, identifies common log levels (ERROR, WARNING, INFO), and highlights the most frequent unique lines, giving you a quick overview of your system's health and potential issues.

## Features

*   **Log Level Counting**: Automatically counts occurrences of 'ERROR', 'WARNING', and 'INFO' messages (case-insensitive).
*   **Unique Line Frequency**: Identifies and ranks the most frequent unique lines in the log file.
*   **Simple CLI**: Easy to use from the command line.

## Usage

```bash
python src/analyzer.py <log_file_path> [--top N]
```

*   `<log_file_path>`: The path to the log file you want to analyze.
*   `--top N`: (Optional) Display the top N most frequent unique lines. Defaults to 5 if not specified.

### Example

```bash
python src/analyzer.py /var/log/syslog --top 10
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `nightly-data-debris-analyzer` directory.
2.  Run the script directly:
    ```bash
    python src/analyzer.py /path/to/your/log.log
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_analyzer.py
```
