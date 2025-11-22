# Nightly Temporal Anomaly Detector

## 🕰️ Purpose

The Nightly Temporal Anomaly Detector is a whimsical-yet-useful utility designed to help you identify files in your project that haven't been modified in a significant amount of time. In the post-apocalyptic digital landscape, forgotten files can accumulate like digital dust, consuming precious storage and obscuring active development. This tool helps you spot these "temporal anomalies" – files that might be stale, obsolete, or simply forgotten – so you can decide whether to archive, delete, or re-evaluate their purpose.

Keep your digital bunker tidy and efficient!

## 🚀 Usage

Run the detector from your terminal, specifying the directory to scan and the number of days to consider a file "stale."

```bash
python src/detector.py --path /path/to/your/project --days 90
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--days <integer>`: The number of days after which a file is considered "stale" if not modified. (Default: 90)

## 💡 Example Output

```
Scanning /path/to/your/project for files not modified in 90 days...

Temporal Anomalies Detected:
- /path/to/your/project/old_config.bak (Last Modified: 2023-01-15 10:30:00)
- /path/to/your/project/docs/draft_v1.txt (Last Modified: 2022-11-01 14:00:00)
- /path/to/your/project/legacy/unused_script.py (Last Modified: 2023-02-28 09:15:00)

Consider reviewing, archiving, or deleting these files to maintain a lean and efficient project.
```

## 🛠️ Development

This utility is written in Python 3.11 and uses only standard library modules.

### Running Tests

```bash
python -m unittest tests/test_detector.py
```
