# Temporal Anomaly Detector

## Overview

The `temporal-anomaly-detector` is a whimsical-yet-useful utility designed to scan your file system for unusual timestamp patterns, which we playfully call "temporal anomalies." While it won't prevent a paradox, it can help identify files that might have been tampered with, incorrectly copied, or are simply misconfigured in terms of their modification and creation times. Think of it as a digital chronometer for your files, ensuring they're not out of sync with the current timeline.

## Features

*   **Future Modification Detection**: Flags files whose modification timestamp is set to a time in the future. This can indicate system clock issues, malicious activity, or accidental misconfigurations.
*   **Future Creation Detection**: Identifies files whose creation timestamp is set to a time in the future. Similar to future modification, this is often a sign of underlying system problems.
*   **Retroactive Modification Detection**: Points out files where the modification timestamp is older than the creation timestamp. While sometimes legitimate (e.g., copying a file and preserving its original modification date), it's an unusual pattern that warrants investigation, especially for newly created files.

## Installation

This utility is self-contained and written in Python 3.11. No special installation steps are required beyond having a compatible Python environment.

## Usage

To run the detector, simply execute the `detector.py` script with the target directory as an argument:

```bash
python src/detector.py /path/to/your/directory
```

### Example Output (No Anomalies)

```
Scanning '/path/to/your/directory' for temporal anomalies...

No temporal anomalies detected. All timelines appear stable.
```

### Example Output (Anomalies Detected)

If anomalies are found, the utility will print a JSON array detailing each anomaly and exit with a non-zero status code (1).

```json
Scanning '/path/to/your/directory' for temporal anomalies...

--- Temporal Anomalies Detected! ---
[
  {
    "file": "/path/to/your/directory/future_report.txt",
    "type": "Future Modification",
    "description": "File modified in the future: 2024-01-01T00:00:00",
    "mtime": "2024-01-01T00:00:00",
    "ctime": "2023-10-27T10:00:00",
    "current_time": "2023-10-27T10:00:00"
  },
  {
    "file": "/path/to/your/directory/old_log.log",
    "type": "Retroactive Modification",
    "description": "File modification time (2023-01-01T00:00:00) is older than its creation time (2023-10-27T10:00:00)",
    "mtime": "2023-01-01T00:00:00",
    "ctime": "2023-10-27T10:00:00",
    "current_time": "2023-10-27T10:00:00"
  }
]
```

## Why is this useful?

*   **Security Auditing**: Unexplained future timestamps or retroactive modifications can be indicators of system compromise, time-bomb malware, or attempts to obscure activity.
*   **Data Integrity**: Helps ensure that backups, archives, and synchronized folders maintain consistent and logical timestamp data.
*   **Debugging**: Can assist in diagnosing issues related to build systems, caching mechanisms, or deployment pipelines that rely heavily on file timestamps.
*   **System Health**: Identifies potential clock synchronization problems on servers or development machines.

## Development

The utility is written in Python and uses standard library modules (`os`, `datetime`, `json`).
Tests are located in `tests/test_detector.py` and use `unittest` with `unittest.mock` for deterministic, offline execution.
