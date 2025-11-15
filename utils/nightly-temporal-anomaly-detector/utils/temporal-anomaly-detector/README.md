# Temporal Anomaly Detector

## Overview

The `Temporal Anomaly Detector` is a whimsical-yet-useful utility designed to scan your file system for unusual file modification and creation timestamps. In the grand scheme of impending apocalypses, a misconfigured system clock or tampered file timestamps could be an early warning sign of a temporal distortion, a rogue AI attempting to rewrite history, or simply a misbehaving backup script.

This tool helps identify:
1.  **Future Anomalies**: Files whose modification times are set significantly in the future. This can indicate system clock issues, file corruption, or even malicious attempts to evade detection.
2.  **Past-Modified Anomalies**: Files that were created a very long time ago but have been modified very recently. While sometimes legitimate (e.g., updating an old config file), this pattern can also signal suspicious activity, such as an attacker modifying historical logs or injecting code into dormant system files.

By detecting these "temporal anomalies," you can maintain a tighter grip on your system's integrity and potentially uncover subtle signs of impending digital doom.

## Usage

The detector is a Python 3.11 script that can be run from the command line.

### Prerequisites

*   Python 3.11 or higher

### Running the Detector

Navigate to the `utils/temporal-anomaly-detector/` directory and run the `detector.py` script:

```bash
python src/detector.py <path_to_scan> [OPTIONS]
```

**Arguments:**

*   `<path_to_scan>`: The root directory from which to start scanning for files.

**Options:**

*   `--future-days <int>`: (Default: `1`) Defines the threshold in days for considering a file's modification time to be "in the future." If a file's `mtime` is more than this many days ahead of the current time, it's flagged.
*   `--old-modified-days <int>`: (Default: `365`) Defines the threshold in days for considering a file's creation time (`ctime`) to be "old." If a file's `ctime` is older than this many days, it's a candidate for a "past-modified" anomaly.
*   `--recent-window-days <int>`: (Default: `7`) Defines the window in days for "recent modification." If an "old" file (per `--old-modified-days`) has been modified within this many days, it's flagged as a "past-modified" anomaly.

### Examples

Scan your current directory for anomalies with default settings:

```bash
python src/detector.py .
```

Scan `/var/log` and be more sensitive to future dates (e.g., 1 day ahead) and very old files modified in the last day:

```bash
python src/detector.py /var/log --future-days 1 --old-modified-days 730 --recent-window-days 1
```

### Output

The script outputs a JSON object to `stdout` containing two lists: `future_anomalies` and `past_modified_anomalies`. Each entry includes the file path, its relevant timestamp(s), and a reason for flagging.

```json
{
  "future_anomalies": [
    {
      "path": "/mock/scan/path/future_file.txt",
      "mtime": "2024-01-01T12:00:00",
      "reason": "Modification time is 2 days in the future."
    }
  ],
  "past_modified_anomalies": [
    {
      "path": "/mock/scan/path/old_but_new.log",
      "mtime": "2023-12-25T10:00:00",
      "ctime": "2022-01-01T08:00:00",
      "reason": "File created over 365 days ago, but modified within the last 7 days."
    }
  ]
}
```

## Development

### Running Tests

To run the automated tests, navigate to the `utils/temporal-anomaly-detector/` directory and execute:

```bash
python -m unittest tests/test_detector.py
```

The tests use `unittest.mock` to simulate file system interactions, ensuring they are deterministic and do not require actual file system changes.
