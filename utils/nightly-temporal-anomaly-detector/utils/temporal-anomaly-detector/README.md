# Temporal Anomaly Detector

A whimsical-yet-useful utility to scan your file system for "temporal anomalies" – files with modification timestamps set in the future. This can be a symptom of system clock issues, corrupted file metadata, or even a mischievous time-traveling squirrel. Identifying these anomalies can prevent build failures, caching issues, or general data inconsistencies.

## Usage

The utility is a Python 3.11 script that takes one or more directory paths as arguments.

```bash
python src/detector.py <directory1> [directory2 ...]
```

### Example

To scan your current directory and a specific project folder:

```bash
python src/detector.py . /home/user/my_project
```

### Expected Output

**If no anomalies are found:**

```
Scanning directories: ., /home/user/my_project
No temporal anomalies detected. All timestamps are in order.
```

**If anomalies are found:**

```
Scanning directories: ., /home/user/my_project

--- Temporal Anomalies Detected! ---
- /home/user/my_project/build/future_artifact.zip
- ./temp/log_2024-01-01_future.txt

Consider checking your system clock or file timestamps.
```

The script will exit with code `0` if no anomalies are found, and `1` if any temporal anomalies are detected.

## How it Works

The `detector.py` script walks through the specified directories, checking the modification time (`mtime`) of each file. It compares this `mtime` against the current system time. If a file's `mtime` is later than the current time, it's flagged as a temporal anomaly.

## Development & Testing

The utility is self-contained and uses standard Python libraries (`os`, `datetime`, `argparse`).

To run tests:

```bash
python -m unittest tests/test_detector.py
```

Tests are deterministic and use `unittest.mock` to simulate file system operations and control the "current time" for consistent results.
