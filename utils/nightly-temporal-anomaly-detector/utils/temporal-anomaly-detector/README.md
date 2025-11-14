# Temporal Anomaly Detector

## Overview

The `temporal-anomaly-detector` is a whimsical-yet-useful utility designed to help you maintain digital hygiene by identifying files that are either suspiciously old or suspiciously new within a given directory. Think of it as a time-traveling lint tool for your file system!

It scans a specified directory and flags files whose last modification timestamp falls outside a configurable 'normal' temporal window. This can be invaluable for:

*   **Cleaning up stale data**: Discovering forgotten log files, old backups, or cached data that's taking up space.
*   **Spotting recent changes**: Highlighting files that were modified very recently, which might indicate active development, a new deployment, or even an unexpected intrusion.
*   **Maintaining order**: Ensuring your project directories don't accumulate 'temporal anomalies' that could lead to confusion or performance issues.

## Usage

```bash
python src/anomaly_detector.py <directory_path> [--max-age-days <days>] [--min-age-seconds <seconds>]
```

### Arguments:

*   `<directory_path>`: The path to the directory you want to scan for temporal anomalies.
*   `--max-age-days <days>`: (Optional) Files older than this many days will be flagged as 'TOO_OLD'. Default is `30` days.
*   `--min-age-seconds <seconds>`: (Optional) Files newer than this many seconds (from now) will be flagged as 'TOO_NEW'. Default is `60` seconds.

### Examples:

Scan the current directory, flagging files older than 7 days or newer than 30 seconds:

```bash
python src/anomaly_detector.py . --max-age-days 7 --min-age-seconds 30
```

Scan a specific log directory, only looking for files older than 90 days:

```bash
python src/anomaly_detector.py /var/log --max-age-days 90 --min-age-seconds 0
```

## Output

The utility will print a list of detected anomalies, including the file path, the type of anomaly (TOO_OLD or TOO_NEW), and its modification timestamp.

```
Temporal Anomaly Report for: /path/to/scan
-----------------------------------------
[TOO_OLD] /path/to/scan/old_report.log (Modified: 2023-01-15 10:00:00)
[TOO_NEW] /path/to/scan/temp_file.tmp (Modified: 2024-07-20 14:35:10)
-----------------------------------------
No anomalies detected.
```

## Development

To run tests:

```bash
python -m unittest tests/test_anomaly_detector.py
```
