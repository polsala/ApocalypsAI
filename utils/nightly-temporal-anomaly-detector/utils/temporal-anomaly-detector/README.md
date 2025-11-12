# Temporal Anomaly Detector

## 🕰️ Uncover Chronological Quirks in Your Filesystem! 🕰️

Have you ever suspected your files might be... out of sync with the fabric of spacetime? The Temporal Anomaly Detector is here to help! This whimsical-yet-useful utility scans a specified directory for files exhibiting unusual timestamp patterns, which we affectionately call "temporal anomalies."

While it won't reveal time-traveling documents (probably), it's excellent for spotting:
*   Files modified *before* they were created (a common sign of specific copy operations or filesystem weirdness).
*   Files with creation or modification dates far in the future or distant past, potentially indicating clock synchronization issues, data corruption, or mischievous temporal distortions.

Keep your digital timeline pristine and catch those chronological paradoxes before they unravel your repository!

## ✨ Features

*   **Anomaly Detection**: Flags files where `mtime < ctime`.
*   **Future/Past Timestamp Check**: Identifies files with timestamps significantly deviating from the current system time.
*   **Configurable Thresholds**: Adjust what constitutes a "significant" deviation.
*   **Simple CLI**: Easy to run and integrate into your nightly checks.

## 🚀 Usage

```bash
python src/anomaly_detector.py --path /path/to/scan [--future-threshold-hours 24] [--past-threshold-years 10] [--verbose]
```

### Arguments:
*   `--path <directory>`: The directory to scan for temporal anomalies. (Required)
*   `--future-threshold-hours <int>`: Files with timestamps more than this many hours in the future will be flagged. Default: `24`.
*   `--past-threshold-years <int>`: Files with timestamps more than this many years in the past will be flagged. Default: `10`.
*   `--verbose`: Print details for all scanned files, not just anomalies.

## 🛠️ Development

The utility is written in Python 3.11 and uses standard library modules only.

### Running Tests

```bash
python -m unittest tests/test_anomaly_detector.py
```

## 📜 License

This utility is released under the MIT License. See `LICENSE` in the repository root for more details.
