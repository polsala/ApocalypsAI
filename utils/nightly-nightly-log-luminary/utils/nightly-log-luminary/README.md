# Nightly Log Luminary

## Overview

In the digital wasteland, log files can be a cryptic mess, hiding vital clues about your system's health or impending doom. The Nightly Log Luminary is here to shine a light on that chaos, providing clear, concise summaries and highlighting critical events so you can quickly understand what's happening under the hood.

This utility processes log files, identifies common log levels (ERROR, WARNING, INFO, DEBUG), and generates a summary report, making it easier to spot anomalies and keep your systems running, even when the world outside is falling apart.

## Usage

```bash
python src/luminary.py --log-file /path/to/your/application.log [--output-file /path/to/report.txt] [--pattern "regex_pattern"] [--case-sensitive]
```

### Arguments:

*   `--log-file`: **Required**. Path to the log file to analyze.
*   `--output-file`: **Optional**. Path to save the analysis report. If not provided, the report will be printed to the console.
*   `--pattern`: **Optional**. A custom regular expression pattern to search for in log lines. If matched, these lines will be highlighted in the summary. Can be specified multiple times.
*   `--case-sensitive`: **Optional**. Make pattern matching case-sensitive. By default, it's case-insensitive.

## Example

```bash
# Analyze a log file and print to console
python src/luminary.py --log-file my_app.log

# Analyze a log file, save report, and look for 'DatabaseError'
python src/luminary.py --log-file server.log --output-file server_report.txt --pattern "DatabaseError"

# Analyze a log file with multiple custom patterns
python src/luminary.py --log-file system.log --pattern "CRITICAL" --pattern "Failed login attempt"
```

## Report Structure

The generated report will include:

*   Total lines processed.
*   Counts for standard log levels (ERROR, WARNING, INFO, DEBUG).
*   Counts for each custom pattern matched.
*   A list of the first few (e.g., 10) lines matching 'ERROR' or custom patterns, for quick inspection.

## Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

## Tests

To run the tests, navigate to the `utils/nightly-log-luminary` directory and execute:

```bash
python -m unittest tests/test_luminary.py
```
