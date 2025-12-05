# Nightly Temporal Anomaly Detector

## Overview

The `nightly-temporal-anomaly-detector` is a whimsical-yet-useful utility designed to help you spot temporal inconsistencies in your file system. In a world where time itself might be fractured, ensuring your files aren't living in the future (or the distant past) is crucial for data integrity and system health.

This tool scans a specified directory for files whose modification timestamps (`mtime`) are suspiciously out of sync with the present. It's particularly useful for identifying:
*   Files with modification dates in the future, often indicating a misconfigured system clock or file system corruption.
*   Files with extremely ancient modification dates (e.g., before 1980), which can also point to corruption or default timestamps.

Keep your digital chronicles in order, even when the timeline gets wobbly!

## Usage

```bash
python src/detector.py <directory_path> [--future-threshold <seconds>] [--ancient-year <year>] [--no-recursive]
```

### Arguments:

*   `<directory_path>`: The path to the directory to scan.
*   `--future-threshold <seconds>`: (Optional) Number of seconds into the future a file's `mtime` can be before it's flagged. Default is `5` seconds. This accounts for minor clock drift.
*   `--ancient-year <year>`: (Optional) Files modified before this year will be flagged as ancient. Default is `1980`.
*   `--no-recursive`: (Optional) If set, the scanner will only check the top-level directory and not recurse into subdirectories.

### Examples:

Scan the current directory for anomalies:
```bash
python src/detector.py .
```

Scan a specific directory, allowing for a 60-second future drift:
```bash
python src/detector.py /var/log --future-threshold 60
```

Scan a directory, flagging files older than 1990, non-recursively:
```bash
python src/detector.py /tmp --ancient-year 1990 --no-recursive
```

## Development

To run tests:
```bash
python -m unittest tests/test_detector.py
```
