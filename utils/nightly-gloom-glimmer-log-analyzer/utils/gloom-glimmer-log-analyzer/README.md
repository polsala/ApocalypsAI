# Gloom-Glimmer Log Analyzer

The Gloom-Glimmer Log Analyzer is a whimsical-yet-useful utility designed to help you quickly sift through the digital rubble of your system logs. It scans specified log files for predefined or custom keywords (like "ERROR", "WARNING", "CRITICAL") and generates a concise summary report, highlighting potential issues and giving you a glimmer of insight into your system's health amidst the gloom.

## Features

*   **Keyword Scanning**: Easily identify important messages (errors, warnings, custom alerts) in your log files.
*   **Case-Insensitive Search**: Finds keywords regardless of their casing.
*   **Multiple File Support**: Analyze one or many log files in a single run.
*   **Detailed & Overall Summaries**: Get per-file breakdowns and a consolidated report of all findings.
*   **Flexible Output**: View reports in a human-readable format or as structured JSON for programmatic use.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having a compatible Python environment.

## Usage

Navigate to the `utils/gloom-glimmer-log-analyzer` directory and run the `analyzer.py` script.

```bash
python src/analyzer.py <log_file_1> [log_file_2 ...] [--keywords <keyword_1> <keyword_2> ...] [--json]
```

### Arguments:

*   `<log_file_1> [log_file_2 ...]`: One or more paths to the log files you want to analyze.
*   `--keywords <keyword_1> <keyword_2> ...`: (Optional) Specify custom keywords to search for. If not provided, it defaults to `ERROR WARNING CRITICAL`.
*   `--json`: (Optional) Output the report in JSON format. By default, it prints a human-readable text report.

### Examples:

1.  **Analyze a single log file with default keywords:**
    ```bash
    python src/analyzer.py /var/log/syslog
    ```

2.  **Analyze multiple log files with default keywords:**
    ```bash
    python src/analyzer.py /var/log/auth.log /var/log/kern.log
    ```

3.  **Analyze a log file with custom keywords:**
    ```bash
    python src/analyzer.py myapp.log --keywords "FAILURE" "ALERT" "DENIED"
    ```

4.  **Get a JSON report for a log file:**
    ```bash
    python src/analyzer.py /var/log/nginx/error.log --json
    ```

5.  **Combine custom keywords and JSON output:**
    ```bash
    python src/analyzer.py /var/log/apache2/access.log --keywords "404" "500" --json
    ```

## Output Format (Text)

```
--- Gloom-Glimmer Log Analysis Report ---
Total files scanned: 2
Files with issues: 1

--- File-specific Reports ---

File: myapp.log
  ERROR: 2
  WARNING: 1
  CRITICAL: 0
  Total matches in file: 3

File: other.log
  ERROR: 0
  WARNING: 0
  CRITICAL: 0
  Total matches in file: 0

--- Overall Summary ---
  ERROR: 2
  WARNING: 1
  CRITICAL: 0
  Total matches overall: 3
---------------------------------------
```

## Output Format (JSON)

```json
{
  "total_files_scanned": 2,
  "files_with_issues": 1,
  "report": {
    "myapp.log": {
      "ERROR": 2,
      "WARNING": 1,
      "CRITICAL": 0,
      "total_matches": 3
    },
    "other.log": {
      "ERROR": 0,
      "WARNING": 0,
      "CRITICAL": 0,
      "total_matches": 0
    }
  },
  "overall_summary": {
    "ERROR": 2,
    "WARNING": 1,
    "CRITICAL": 0,
    "total_matches": 3
  }
}
```

## Development & Testing

To run the tests, navigate to the `utils/gloom-glimmer-log-analyzer` directory and execute:

```bash
python -m unittest tests/test_analyzer.py
```

All tests are designed to be deterministic and run offline using Python's `unittest.mock` library to simulate file system interactions.
