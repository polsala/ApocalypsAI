# Temporal Anomaly Detector

## Unearthing Chronological Oddities in Your Filesystem

In the chaotic aftermath, even your file timestamps can betray you. The `Temporal Anomaly Detector` is a whimsical-yet-useful utility designed to scan your directories for files that exist *ahead of their time* – files whose modification timestamps are set in the future. This can be a tell-tale sign of system clock desynchronization, corrupted file metadata, or even a mischievous temporal ripple.

Catch these chronological paradoxes before they unravel your build processes or lead to unexpected data inconsistencies!

## Usage

Run the script with the path to the directory you wish to scan:

```bash
python src/detector.py /path/to/your/directory
```

### Example Output

```
Scanning /path/to/your/directory for temporal anomalies...

Anomaly Detected: /path/to/your/directory/future_log.txt (Modified: 2025-01-01 10:00:00)
Anomaly Detected: /path/to/your/directory/build_cache/next_version.tmp (Modified: 2024-12-25 08:30:00)
No further anomalies found.
Scan complete. 2 anomalies detected.
```

If no anomalies are found, it will simply report that the timeline is stable.
