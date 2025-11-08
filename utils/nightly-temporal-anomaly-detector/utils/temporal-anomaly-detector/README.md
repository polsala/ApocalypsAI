# Temporal Anomaly Detector

## 🕰️ Unearthing Chronological Oddities in Your Filesystem 🕰️

The ApocalypsAI Nightly Integrator presents the Temporal Anomaly Detector – a whimsical-yet-useful utility designed to scan your file system for unusual discrepancies between file modification times (`mtime`) and metadata change times (`ctime`). In the grand scheme of things, a file's content and its metadata usually evolve in a somewhat synchronized fashion. When they don't, it might be a subtle whisper of tampering, a system out of sync, or even a hint of data corruption.

Think of it as a digital chronometer for your files, alerting you to "time jumps" or "temporal paradoxes" that could signify something amiss in the fabric of your data.

## ✨ Features

*   **Chronological Discrepancy Detection**: Identifies files where the absolute difference between `mtime` and `ctime` exceeds a configurable threshold.
*   **"Time Warp" Alerts**: Specifically flags files where `mtime` appears to be *older* than `ctime`, a common indicator of restoration from older backups or manual date manipulation.
*   **Recursive Scanning**: Traverses directories and subdirectories to ensure no temporal anomaly goes unnoticed.
*   **Configurable Threshold**: Adjust the sensitivity of the detector to suit your needs.

## 🚀 Usage

The utility is a simple Python script.

```bash
python src/detector.py --path /path/to/scan [--threshold-seconds <seconds>]
```

*   `--path`: The directory to start scanning from. (Required)
*   `--threshold-seconds`: The maximum allowed absolute difference between `mtime` and `ctime` in seconds. Defaults to `86400` (24 hours).

### Example

Scan your `documents` folder for anomalies exceeding a 1-hour difference:

```bash
python src/detector.py --path ~/documents --threshold-seconds 3600
```

Scan your entire system (use with caution and appropriate permissions!):

```bash
sudo python src/detector.py --path / --threshold-seconds 600
```

### Output

The script will print any detected anomalies to standard output, indicating the file path, its `mtime`, `ctime`, and the calculated difference.

```
[ANOMALY] /path/to/file.txt: mtime=2023-01-01 10:00:00, ctime=2024-01-01 10:00:00, Diff=-31536000.0s (mtime significantly older than ctime)
[ANOMALY] /path/to/another_file.log: mtime=2024-01-01 12:30:00, ctime=2024-01-01 10:00:00, Diff=9000.0s (large positive difference)
```

## 🛠️ Development

To run tests:

```bash
python -m unittest tests/test_detector.py
```
