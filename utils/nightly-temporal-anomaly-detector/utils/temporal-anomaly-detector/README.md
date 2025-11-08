# Temporal Anomaly Detector

A whimsical-yet-useful Python CLI utility to monitor your digital spacetime for unexpected disruptions. The Temporal Anomaly Detector helps you keep an eye on critical files and directories, reporting 'anomalies' such as:

*   Files that haven't been modified in an unusually long time.
*   Unexpected new files appearing in a monitored directory.
*   Missing files or directories.

It's like a cosmic alarm system for your file system, ensuring your data streams flow as expected!

## Installation

This utility is self-contained and requires Python 3.8+.
No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/temporal-anomaly-detector` directory.
2.  (Optional, but recommended) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

## Usage

Run the `detector.py` script with the path you wish to monitor.

```bash
python3 src/detector.py --path <file_or_directory_path> [options]
```

### Options

*   `--path <path>` (required): The file or directory path to monitor.
*   `--max-age-days <days>`: Report a file as an anomaly if its last modification time is older than this many days.
*   `--expect-pattern <regex_pattern>`: (For directories) A regex pattern that all expected filenames should match. Files not matching this pattern will be reported as anomalies. Can be specified multiple times for multiple patterns.
*   `--verbose`: Print more detailed information, even for non-anomalous items.

### Examples

1.  **Check if a log file is still being updated (max 1 day old):**
    ```bash
    python3 src/detector.py --path /var/log/my_app.log --max-age-days 1
    ```

2.  **Monitor a data directory for unexpected new files (expecting only `.csv` files):**
    ```bash
    python3 src/detector.py --path /data/reports --expect-pattern ".*\.csv$"
    ```

3.  **Monitor a configuration directory for any file older than 7 days:**
    ```bash
    python3 src/detector.py --path /etc/my_service --max-age-days 7
    ```

4.  **Combined check for a directory:**
    ```bash
    python3 src/detector.py --path /tmp/staging --max-age-days 0.5 --expect-pattern "upload_.*\.zip$"
    ```

## Development & Testing

To run the tests:

```bash
python3 -m unittest tests/test_detector.py
```
