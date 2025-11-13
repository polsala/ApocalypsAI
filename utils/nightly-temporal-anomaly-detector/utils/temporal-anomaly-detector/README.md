# Temporal Anomaly Detector

## Overview

Welcome, intrepid archivist! Have you ever felt a shiver down your spine, a subtle ripple in the fabric of your digital reality, suggesting that some files are simply... out of place? The **Temporal Anomaly Detector** is your first line of defense against such chronological disarray.

This whimsical-yet-useful utility scans a specified directory for files whose modification times are either suspiciously ancient or alarmingly fresh, relative to a threshold you define. Whether you're hunting for forgotten relics that predate your memory or suspicious newcomers that appeared just moments ago, this tool helps you pinpoint them.

Think of it as a time-traveling librarian, ensuring every file is in its proper temporal shelf.

## Usage

### Prerequisites

*   Python 3.11+

### Running the Detector

Navigate to the `src` directory and run the `anomaly_detector.py` script. You must provide a directory to scan and a temporal threshold.

```bash
python src/anomaly_detector.py --help
```

```
usage: anomaly_detector.py [-h] --path PATH (--older-than OLDER_THAN | --newer-than NEWER_THAN) {days,hours,minutes}

A whimsical utility to detect files with 'anomalous' modification times.

positional arguments:
  {days,hours,minutes}  Unit for the temporal threshold.

options:
  -h, --help            show this help message and exit
  --path PATH           The directory path to scan for temporal anomalies.
  --older-than OLDER_THAN
                        Detect files older than this value.
  --newer-than NEWER_THAN
                        Detect files newer than this value.
```

### Examples

1.  **Find files older than 30 days in your 'documents' folder:**

    ```bash
    python src/anomaly_detector.py --path /home/user/documents --older-than 30 days
    ```

2.  **Identify files created or modified in the last 2 hours in your 'downloads' folder:**

    ```bash
    python src/anomaly_detector.py --path /home/user/downloads --newer-than 2 hours
    ```

3.  **Check for files modified within the last 5 minutes in a critical log directory:**

    ```bash
    python src/anomaly_detector.py --path /var/log/app --newer-than 5 minutes
    ```

## How it Works

The script calculates a temporal threshold based on your input (e.g., 30 days ago from now). It then iterates through all files in the specified directory, comparing each file's last modification timestamp against this threshold. Files that fall outside the normal temporal bounds (either too old or too new) are flagged as 'anomalies' and reported.

## Contributing

Feel free to enhance the temporal detection algorithms, add more whimsical anomaly types, or improve the reporting mechanisms. All contributions to maintaining temporal integrity are welcome!
