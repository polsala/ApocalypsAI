# nightly-log-whisperer

A whimsical yet useful bash script designed to sift through log files and identify potential anomalies or interesting patterns, affectionately termed 'whispers'. It's like having a tiny, spectral archivist for your system logs.

## Features

*   **Pattern Detection**: Looks for common error indicators (e.g., 'ERROR', 'WARN', 'FAIL', 'exception').
*   **Frequency Analysis**: Highlights lines that appear unusually frequently, suggesting potential loops or repeated issues.
*   **Customizable Keywords**: Allows users to define their own keywords to search for.
*   **Output Formatting**: Presents findings in a human-readable format, highlighting the 'whispers'.

## Usage

```bash
./nightly-log-whisperer <log_file_path> [keyword1 keyword2 ...]
```

*   `<log_file_path>`: The path to the log file you want to analyze.
*   `[keyword1 keyword2 ...]`: Optional. A list of custom keywords to search for in addition to the default ones.

## Examples

Analyze a system log for errors and warnings:

```bash
./nightly-log-whisperer /var/log/syslog
```

Analyze an application log for specific errors and a custom 'critical' keyword:

```bash
./nightly-log-whisperer /var/log/myapp.log ERROR WARN FAIL CRITICAL
```

## How it Works

The script uses standard bash utilities like `grep`, `awk`, and `sort` to process the log file. It first identifies lines containing predefined or user-specified keywords. Then, it performs a frequency analysis on these lines to spot any that might be occurring too often. Finally, it outputs the findings in a structured way.

## Testing

Tests are included in the `tests/` directory. They use mock log files to ensure deterministic and offline execution.

To run tests:

```bash
cd utils/nightly-log-whisperer
bash tests/run_tests.sh
```
