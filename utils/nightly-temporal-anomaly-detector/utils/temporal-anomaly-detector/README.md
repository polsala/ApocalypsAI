# Temporal Anomaly Detector

A whimsical-yet-useful utility for the ApocalypsAI community, designed to detect "temporal anomalies" in your filesystem.

## 🌌 What is a Temporal Anomaly?

In the vast, chaotic expanse of your digital universe, a "temporal anomaly" refers to a file whose last modification timestamp (`mtime`) is set to a point in the *future* relative to your system's current clock. While not a sign of impending doom (usually), these anomalies can indicate:

*   **Clock Synchronization Issues**: Your system clock might be out of sync, or files were copied from a system with a different time.
*   **Filesystem Corruption**: Rare, but possible.
*   **Build System Headaches**: Tools like `make` or `rsync` rely heavily on modification times. A future timestamp can cause files to be perpetually rebuilt or skipped incorrectly.
*   **Time Travelers**: Less likely, but we can't rule it out.

This utility helps you identify and address these discrepancies before they cause more significant issues in your workflows or, you know, the actual apocalypse.

## 🚀 Usage

The `temporal-anomaly-detector` is a Python 3.11+ script.

### Prerequisites

*   Python 3.11+

### Running the Detector

1.  Navigate to the `utils/temporal-anomaly-detector/` directory.
2.  Run the script, providing the path to the directory you wish to scan:

    ```bash
    python src/detector.py /path/to/your/directory
    ```

    Replace `/path/to/your/directory` with the actual path you want to scan. You can scan your entire home directory, a specific project folder, or even the root (`/`) if you dare (and have permissions!).

### Example Output

```
Scanning '/home/user/my_project' for temporal anomalies...
ANOMALY DETECTED: '/home/user/my_project/build/future_artifact.bin' has future modification time: 2024-01-01 00:00:00
ANOMALY DETECTED: '/home/user/my_project/data/temp_log.txt' has future modification time: 2023-12-31 23:59:59
No temporal anomalies detected. All clear!
```

If no anomalies are found, you'll see a reassuring "No temporal anomalies detected. All clear!" message. If errors occur (e.g., directory not found, permission issues), they will be printed to `stderr`.

## 🛠️ Development & Testing

To run the tests, navigate to the `utils/temporal-anomaly-detector/` directory and execute:

```bash
python -m unittest tests/test_detector.py
```

All tests are self-contained and use `unittest.mock` to simulate filesystem interactions and time, ensuring deterministic and offline execution.
