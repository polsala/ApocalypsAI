# Nightly Temporal Anomaly Detector

## 🌌 Purpose

The Nightly Temporal Anomaly Detector is a whimsical yet crucial utility designed to scan your digital archives for temporal inconsistencies. In the vast cosmic dance of data, files can sometimes drift out of sync, appearing to exist in the future or lingering from an impossibly distant past. This tool helps you identify such "temporal anomalies" – files with modification timestamps that are either ahead of the current system time or significantly older than a defined threshold.

Detecting these anomalies can be vital for:
*   **System Health**: Identifying potential system clock issues or file corruption.
*   **Security Audits**: Spotting files that might have been tampered with or introduced with misleading timestamps.
*   **Data Hygiene**: Pinpointing forgotten relics that might warrant archiving or deletion.

## 🚀 Usage

Run the detector from your terminal, specifying the directory to scan:

```bash
python src/detector.py /path/to/your/directory [--max-age-years <int>] [--future-tolerance-seconds <int>]
```

### Arguments:

*   `<directory>`: The root directory to start scanning.
*   `--max-age-years <int>`: (Optional) Files older than this many years will be flagged as "ancient". Default is 5 years.
*   `--future-tolerance-seconds <int>`: (Optional) Files modified more than this many seconds in the future will be flagged. Default is 60 seconds (to account for minor clock drifts).

### Example:

```bash
python src/detector.py ~/my_documents --max-age-years 10 --future-tolerance-seconds 300
```

This will scan `~/my_documents` for files modified over 10 years ago or more than 5 minutes in the future.

## 🛠️ Development

The detector is written in Python 3.11 and uses standard library modules only.

### Running Tests:

Navigate to the `utils/nightly-temporal-anomaly-detector` directory and run:

```bash
python -m unittest tests/test_detector.py
```
