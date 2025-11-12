# Nightly Temporal Anomaly Detector

## Overview

The `nightly-temporal-anomaly-detector` is a whimsical-yet-useful utility designed to scan specified directories for files whose modification timestamps (`mtime`) are suspiciously far in the future or past. While it might sound like a tool for detecting time-traveler interference, its practical purpose is to help identify:

*   **System Clock Drift**: Inaccurate system clocks can lead to future-dated files, causing build issues or unexpected behavior.
*   **File Corruption**: Corrupted file systems might report incorrect timestamps.
*   **Misconfigured Processes**: Build tools or scripts sometimes inadvertently set future dates on generated files.

By flagging these "temporal anomalies," this utility helps maintain the integrity and consistency of your repository's file system.

## Usage

To run the detector, simply execute the `detector.py` script with the target directory:

```bash
python3 src/detector.py --path /path/to/scan
```

### Arguments

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--future-threshold <days>` (optional): Number of days into the future a file's `mtime` can be before it's flagged. Default: `7` days.
*   `--past-threshold <days>` (optional): Number of days into the past a file's `mtime` can be before it's flagged. Default: `30` days.

### Example Output

```
Scanning directory: /home/user/my_repo

--- Temporal Anomalies Detected ---

[FUTURE ANOMALY] /home/user/my_repo/build/future_report.log (Modified: 2025-01-01 12:00:00 UTC)
  Rationale: File's modification time is 365 days in the future.

[PAST ANOMALY] /home/user/my_repo/old_data/legacy_archive.zip (Modified: 1999-12-31 23:59:59 UTC)
  Rationale: File's modification time is 8766 days in the past.

--- Scan Complete ---
Total anomalies found: 2
```

## Development

This utility is written in Python 3.11 and uses only standard library modules (`os`, `datetime`, `time`, `argparse`).

## Testing

Tests are located in `tests/test_detector.py` and can be run using `unittest`:

```bash
python3 -m unittest tests/test_detector.py
```
