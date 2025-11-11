# Nightly Temporal Anomaly Detector

## Overview

The `nightly-temporal-anomaly-detector` is a whimsical-yet-useful Python utility designed to scan a specified directory for unusual temporal patterns in file metadata. It helps identify potential system clock synchronization issues, file system corruption, or even subtle signs of tampering by flagging files with:

1.  **Future Timestamps**: Files whose modification (`mtime`) or creation (`ctime`) dates are set in the future relative to the current system time, beyond a configurable threshold.
2.  **Retrograde Modifications**: Files whose modification date (`mtime`) is significantly older than their creation date (`ctime`). While `ctime` on Unix systems refers to metadata change time, a `mtime` much older than `ctime` can still indicate an anomaly or unusual file operation.

While the universe might not be unraveling, keeping an eye on these 'temporal anomalies' can ensure your data remains consistent and your systems are well-calibrated.

## Usage

```bash
python src/anomaly_detector.py --path /path/to/scan
```

### Arguments

*   `--path <directory>`: The absolute or relative path to the directory to scan for temporal anomalies. (Required)
*   `--future-threshold <seconds>`: (Optional) The number of seconds into the future a timestamp can be before being flagged as an anomaly. Defaults to `60` seconds (allowing for minor clock drift).

## Examples

Scan your current directory for anomalies:

```bash
python src/anomaly_detector.py --path .
```

Scan a specific project directory, allowing for a larger future threshold:

```bash
python src/anomaly_detector.py --path /home/user/my_project --future-threshold 300
```

## Installation

This utility is self-contained and requires Python 3.6+.

```bash
# No special installation steps needed. Just run the script directly.
```

## Development

To run tests:

```bash
python -m pytest tests/test_anomaly_detector.py
```
