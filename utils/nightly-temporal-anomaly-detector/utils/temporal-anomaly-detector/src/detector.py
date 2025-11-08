import os
import time
import argparse
from datetime import datetime, timedelta

def get_current_time_utc():
    """Returns the current UTC time as a datetime object."""
    return datetime.utcfromtimestamp(time.time())

def get_file_mtime_utc(filepath):
    """Returns the modification time of a file as a UTC datetime object."""
    try:
        mtime_timestamp = os.path.getmtime(filepath)
        return datetime.utcfromtimestamp(mtime_timestamp)
    except OSError:
        return None # File might have been deleted between os.walk and os.path.getmtime

def scan_directory_for_anomalies(
    directory_path: str,
    future_threshold_seconds: int = 0,
    old_threshold_days: int = 365
) -> list[dict]:
    """
    Scans a directory for files with temporal anomalies.

    Args:
        directory_path: The path to the directory to scan.
        future_threshold_seconds: Files modified more than this many seconds in the future
                                  will be reported as anomalies.
        old_threshold_days: Files modified more than this many days in the past
                            will be reported as anomalies.

    Returns:
        A list of dictionaries, each representing a detected anomaly.
    """
    anomalies = []
    current_time = get_current_time_utc()

    future_threshold_dt = current_time + timedelta(seconds=future_threshold_seconds)
    old_threshold_dt = current_time - timedelta(days=old_threshold_days)

    if not os.path.isdir(directory_path):
        anomalies.append({
            "type": "Path Error",
            "path": directory_path,
            "message": "Directory does not exist or is not a directory."
        })
        return anomalies

    for root, _, files in os.walk(directory_path):
        for file in files:
            filepath = os.path.join(root, file)
            mtime = get_file_mtime_utc(filepath)

            if mtime is None:
                anomalies.append({
                    "type": "File Access Error",
                    "path": filepath,
                    "message": "Could not retrieve modification time."
                })
                continue

            # Check for future modification time
            if mtime > future_threshold_dt:
                time_diff = mtime - current_time
                anomalies.append({
                    "type": "Future Modification",
                    "path": filepath,
                    "mtime": mtime.isoformat(),
                    "message": f"Modified {time_diff.total_seconds():.0f} seconds in the future."
                })

            # Check for excessively old modification time
            if mtime < old_threshold_dt:
                time_diff = current_time - mtime
                anomalies.append({
                    "type": "Excessively Old Modification",
                    "path": filepath,
                    "mtime": mtime.isoformat(),
                    "message": f"Modified {time_diff.days} days ago (older than {old_threshold_days} days threshold)."
                })

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for temporal anomalies in file modification times."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory path to scan for anomalies."
    )
    parser.add_argument(
        "--future-threshold",
        type=int,
        default=0,
        help="Report files modified more than this many seconds in the future (default: 0)."
    )
    parser.add_argument(
        "--old-threshold",
        type=int,
        default=365,
        help="Report files modified more than this many days in the past (default: 365)."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for temporal anomalies...")
    anomalies = scan_directory_for_anomalies(
        args.path,
        args.future_threshold,
        args.old_threshold
    )

    if anomalies:
        print("\n--- Temporal Anomalies Detected! ---")
        for anomaly in anomalies:
            print(f"Type: {anomaly['type']}")
            print(f"Path: {anomaly['path']}")
            if 'mtime' in anomaly: print(f"MTime: {anomaly['mtime']}")
            print(f"Message: {anomaly['message']}\n")
        print("--- End of Anomaly Report ---")
        exit(1) # Indicate failure if anomalies are found
    else:
        print("No temporal anomalies detected. All timelines appear stable.")
        exit(0) # Indicate success

if __name__ == "__main__":
    main()
