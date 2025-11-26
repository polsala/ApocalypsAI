# Nightly Chrono-Sync Anomaly Detector

## 🕰️ What is this?

The Nightly Chrono-Sync Anomaly Detector is a whimsical yet practical utility designed to help you maintain the temporal integrity of your digital files. It scans specified directories for 'chrono-sync anomalies' – files whose modification or creation timestamps are suspiciously out of sync. Think of it as a time-traveling detective for your file system, sniffing out temporal paradoxes before they become full-blown data disasters.

## 🕵️‍♂️ What kind of anomalies does it detect?

1.  **Future-Dated Files**: Files that appear to have been modified or created in the future. This can indicate a misconfigured system clock, issues with file synchronization, or even a mischievous time-traveler leaving digital breadcrumbs.
2.  **Files Much Older Than Parent Directory**: Files whose modification time is significantly older than their parent directory's modification time. This might suggest old files copied into a new location without timestamp updates, or a directory that was recently created around ancient data.
3.  **Files Much Newer Than Parent Directory**: Files whose modification time is significantly newer than their parent directory's modification time. This could point to a directory that hasn't been touched in ages, but suddenly contains a very recent file, or a file that was updated without the directory's timestamp being propagated.

## 🚀 How to Use

```bash
python3 src/detector.py --path /path/to/scan [--threshold-days N]
```

-   `--path`: The root directory from which to start the scan. This is a required argument.
-   `--threshold-days`: (Optional) The number of days to use as a threshold for detecting 'much older' or 'much newer' file anomalies relative to their parent directories. Defaults to `30` days.

### Example:

To scan your entire home directory with a 60-day threshold:

```bash
python3 src/detector.py --path ~/ --threshold-days 60
```

## 🛠️ How it Works

The utility recursively traverses the specified directory, comparing the modification and creation timestamps of files and directories. It uses the current system time as a reference for future-dated files and calculates differences against parent directory timestamps based on the provided threshold.

It reports any detected anomalies to the console, providing the file path, the type of anomaly, and relevant timestamp details.

## 🧪 Development & Testing

Tests are located in `tests/test_detector.py` and use `unittest.mock` to simulate filesystem interactions, ensuring deterministic and offline execution. To run tests:

```bash
python3 -m unittest tests/test_detector.py
```
