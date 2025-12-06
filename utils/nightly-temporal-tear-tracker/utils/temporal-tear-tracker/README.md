# Temporal Tear Tracker

## Description

The ApocalypsAI Nightly Integrator presents the **Temporal Tear Tracker**! In a world where reality itself might be... *fluid*, files can appear from anywhere, at any time. This utility helps you keep track of these 'temporal tears' – new files appearing in a designated directory.

Whether you're monitoring a data drop-off zone, a shared network drive, or just a folder where strange artifacts occasionally manifest, the Temporal Tear Tracker will log their appearance and tell you how long it's been since the last tear in your reality.

It's genuinely useful for: 
- Monitoring directories for new data ingestion.
- Detecting unexpected file creations.
- Keeping an audit log of file arrivals.

## How it Works

1.  **State Management**: The tracker maintains a `state.json` file within its own directory. This file stores a snapshot of the files (and their modification times) seen during the last successful run, along with the timestamp of the last detected 'temporal tear'.
2.  **Directory Scan**: On each run, it scans the specified target directory for all current files.
3.  **Tear Detection**: It compares the current files against the stored snapshot. Any file found in the current scan that was *not* present in the previous snapshot is considered a 'new temporal tear'.
4.  **Logging & Reporting**: New tears are logged to the console, showing the file path and how long ago it appeared. If no new tears are found, it reports the stability of reality and the time elapsed since the last tear.
5.  **State Update**: The `state.json` is updated with the latest directory snapshot and the timestamp of any newly detected tears.

## Usage

To run the Temporal Tear Tracker, specify the directory you wish to monitor using the `--dir` argument.

```bash
python3 src/tracker.py --dir /path/to/your/monitored/directory
```

### Example Output (Initial Run)

```
[INFO] Monitoring directory: /path/to/your/monitored/directory
[INFO] No previous temporal tears detected. Reality is pristine.
[INFO] Current reality scan complete. State saved to utils/temporal-tear-tracker/state.json
```

### Example Output (New Files Detected)

```
[INFO] Monitoring directory: /path/to/your/monitored/directory
[INFO] A new temporal tear has opened!
[INFO]   - New file detected: /path/to/your/monitored/directory/anomaly_report_2024.txt (appeared 15.3 seconds ago)
[INFO]   - New file detected: /path/to/your/monitored/directory/strange_artifact.log (appeared 5.1 seconds ago)
[INFO] Current reality scan complete. State saved to utils/temporal-tear-tracker/state.json
```

### Example Output (No New Files)

```
[INFO] Monitoring directory: /path/to/your/monitored/directory
[INFO] No new temporal tears detected. Reality remains stable.
[INFO] It has been 3600.5 seconds since the last tear.
[INFO] Current reality scan complete. State saved to utils/temporal-tear-tracker/state.json
```
