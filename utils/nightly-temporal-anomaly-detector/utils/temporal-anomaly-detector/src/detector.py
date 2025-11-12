import os
import datetime
import time

def get_file_timestamps(filepath):
    """Retrieves modification and creation timestamps for a given file."""
    try:
        stat = os.stat(filepath)
        return stat.st_mtime, stat.st_ctime
    except FileNotFoundError:
        return None, None

def detect_anomalies(directory_path):
    """
    Scans a directory for files with temporal anomalies.
    Returns a list of dictionaries, each describing an anomaly.
    """
    anomalies = []
    current_time_ts = datetime.datetime.now().timestamp()

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            mtime_ts, ctime_ts = get_file_timestamps(filepath)

            if mtime_ts is None or ctime_ts is None:
                continue # Skip if file not found or inaccessible

            # Convert timestamps to datetime objects for easier comparison/reporting
            mtime_dt = datetime.datetime.fromtimestamp(mtime_ts)
            ctime_dt = datetime.datetime.fromtimestamp(ctime_ts)
            current_dt = datetime.datetime.fromtimestamp(current_time_ts)

            # Anomaly 1: Future Modification Time
            if mtime_ts > current_time_ts:
                anomalies.append({
                    "file": filepath,
                    "type": "Future Modification",
                    "description": f"File modified in the future: {mtime_dt}",
                    "mtime": mtime_dt.isoformat(),
                    "ctime": ctime_dt.isoformat(),
                    "current_time": current_dt.isoformat()
                })

            # Anomaly 2: Future Creation Time
            if ctime_ts > current_time_ts:
                anomalies.append({
                    "file": filepath,
                    "type": "Future Creation",
                    "description": f"File created in the future: {ctime_dt}",
                    "mtime": mtime_dt.isoformat(),
                    "ctime": ctime_dt.isoformat(),
                    "current_time": current_dt.isoformat()
                })

            # Anomaly 3: Retroactive Modification (mtime older than ctime)
            # This can happen with file copies that preserve mtime, but it's unusual for a new file.
            if mtime_ts < ctime_ts:
                anomalies.append({
                    "file": filepath,
                    "type": "Retroactive Modification",
                    "description": f"File modification time ({mtime_dt}) is older than its creation time ({ctime_dt})",
                    "mtime": mtime_dt.isoformat(),
                    "ctime": ctime_dt.isoformat(),
                    "current_time": current_dt.isoformat()
                })
    return anomalies

if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python detector.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]
    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found.")
        sys.exit(1)

    print(f"Scanning '{target_directory}' for temporal anomalies...")
    found_anomalies = detect_anomalies(target_directory)

    if found_anomalies:
        print("\n--- Temporal Anomalies Detected! ---")
        print(json.dumps(found_anomalies, indent=2))
        sys.exit(1) # Exit with error code if anomalies are found
    else:
        print("\nNo temporal anomalies detected. All timelines appear stable.")
        sys.exit(0)
