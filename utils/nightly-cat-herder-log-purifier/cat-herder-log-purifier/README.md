# Cat Herder Log Purifier

## Tame the Log Beasts!

In the post-apocalyptic wasteland of distributed systems and salvaged servers, log files can become a chaotic, sprawling mess. The `Cat Herder Log Purifier` is your trusty companion, designed to bring order to the digital pandemonium. It helps you filter, highlight, and summarize log entries, making it easier to spot critical issues amidst the noise.

## Features

*   **Intelligent Parsing**: Automatically detects common log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
*   **Level Filtering**: Show only logs above a certain severity.
*   **Keyword Highlighting**: Emphasize specific terms or phrases.
*   **Summary Statistics**: Get a quick overview of log level distribution.
*   **Color-Coded Output**: Uses `rich` for beautiful, readable console output.

## Installation

This utility requires Python 3.8+ and the `rich` library.

```bash
pip install rich
```

## Usage

```bash
python src/purifier.py <log_file_path> [options]
```

### Examples

1.  **Purify a log file, showing all entries:**

    ```bash
    python src/purifier.py my_app.log
    ```

2.  **Show only WARNING, ERROR, or CRITICAL entries:**

    ```bash
    python src/purifier.py my_app.log --level WARNING
    ```

3.  **Highlight occurrences of 'failed' or 'connection' and show a summary:**

    ```bash
    python src/purifier.py my_app.log --highlight failed connection --summary
    ```

4.  **Combine filters and highlights:**

    ```bash
    python src/purifier.py my_app.log --level ERROR --highlight 'disk full' --summary
    ```

## Options

*   `<log_file_path>`: Path to the log file to purify.
*   `--level <LEVEL>`: Minimum log level to display (DEBUG, INFO, WARNING, ERROR, CRITICAL). Default: DEBUG.
*   `--highlight <KEYWORD> [<KEYWORD> ...]`: One or more keywords to highlight in the output. Case-insensitive.
*   `--summary`: Display a summary of log levels at the end.
*   `--no-color`: Disable color output.

## Example Output

```text
[1] [INFO] Application started successfully.
[2] [DEBUG] Processing request for user_id=123.
[3] [WARNING] Deprecated API call detected in module X.
[4] [ERROR] Database connection [failed] to establish.
[5] [CRITICAL] System shutdown initiated due to unrecoverable error.

--- Log Summary ---
INFO:     1
DEBUG:    1
WARNING:  1
ERROR:    1
CRITICAL: 1
Total:    5
```
