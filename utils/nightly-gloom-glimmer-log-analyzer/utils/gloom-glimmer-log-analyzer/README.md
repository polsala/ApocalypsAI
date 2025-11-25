# Gloom-Glimmer Log Analyzer

A Python utility for the discerning survivor, designed to scan your system's log files for signs of impending doom ("gloom") or reassuring progress ("glimmer"). In the post-apocalyptic digital wasteland, understanding your system's health is paramount. This tool helps you quickly identify critical issues and celebrate small victories.

## Features

*   **Customizable Keywords**: Define your own "gloom" (e.g., `error`, `fail`, `exception`) and "glimmer" (e.g., `success`, `healthy`, `complete`) keywords.
*   **Case-Insensitive Search**: Finds matches regardless of capitalization.
*   **Line-by-Line Reporting**: Pinpoints the exact lines where gloom or glimmer was detected.
*   **Overall Outlook**: Provides a whimsical summary of your system's perceived health based on the balance of gloom and glimmer.

## Installation

This utility is self-contained and requires Python 3.8+ (tested with 3.11). No external dependencies are strictly required beyond the standard library.

1.  Navigate to the `utils/gloom-glimmer-log-analyzer/` directory.
2.  Ensure you have Python installed.

## Usage

Run the `analyzer.py` script directly from your terminal.

```bash
python src/analyzer.py <filepath> [OPTIONS]
```

### Arguments

*   `<filepath>`: The path to the log file you wish to analyze.

### Options

*   `--gloom-keywords <keyword1> <keyword2> ...`: Space-separated keywords to identify "gloom".
    *   Default: `error fail exception critical denied broken`
*   `--glimmer-keywords <keyword1> <keyword2> ...`: Space-separated keywords to identify "glimmer".
    *   Default: `success complete info healthy ok ready`

### Examples

1.  **Analyze a log file with default keywords:**
    ```bash
    python src/analyzer.py /var/log/syslog
    ```

2.  **Analyze a specific application log with custom keywords:**
    ```bash
    python src/analyzer.py my_app.log --gloom-keywords "crash" "timeout" --glimmer-keywords "startup" "connected"
    ```

3.  **Check a log for only specific errors:**
    ```bash
    python src/analyzer.py debug.log --gloom-keywords "segfault" "memory_leak" --glimmer-keywords ""
    ```
    (Note: Passing an empty string for keywords will result in an empty list for that category.)

## Development & Testing

To run the tests, navigate to the `utils/gloom-glimmer-log-analyzer/` directory and execute:

```bash
python -m unittest tests/test_analyzer.py
```

The tests are designed to be deterministic and offline, using Python's `unittest.mock` to simulate file system interactions.
