import os
import time
import argparse
from datetime import datetime

def find_temporal_anomalies(scan_path: str, future_threshold_seconds: int = 60):
    """
    Scans a directory for temporal anomalies in file metadata.

    Args:
        scan_path (str): The path to the directory to scan.
        future_threshold_seconds (int): Number of seconds into the future a timestamp
                                        can be before being flagged as an anomaly.

    Returns:
        dict: A dictionary containing lists of detected anomalies.
              Keys: 'future_timestamps', 'retrograde_modifications'.
    """
    anomalies = {
        'future_timestamps': [],
        'retrograde_modifications': []
    }

    current_time_epoch = time.time()

    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.")
        return anomalies

    for root, _, files in os.walk(scan_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                stat_info = os.stat(file_path)
                mtime = stat_info.st_mtime
                # ctime on Unix is last metadata change, on Windows it's creation time.
                # For anomaly detection, we treat it as a reference point.
                ctime = stat_info.st_ctime

                # Anomaly 1: Future Timestamps
                # Check if mtime or ctime is significantly in the future
                if mtime > current_time_epoch + future_threshold_seconds:
                    anomalies['future_timestamps'].append({
                        'file': file_path,
                        'type': 'future_mtime',
                        'mtime': datetime.fromtimestamp(mtime).isoformat(),
                        'current_time': datetime.fromtimestamp(current_time_epoch).isoformat()
                    })
                if ctime > current_time_epoch + future_threshold_seconds:
                    anomalies['future_timestamps'].append({
                        'file': file_path,
                        'type': 'future_ctime',
                        'ctime': datetime.fromtimestamp(ctime).isoformat(),
                        'current_time': datetime.fromtimestamp(current_time_epoch).isoformat()
                    })

                # Anomaly 2: Retrograde Modifications (mtime < ctime)
                # A modification time significantly older than creation/metadata-change time
                # can indicate issues like restored backups with old mtimes, or clock resets.
                if mtime < ctime - 1: # Allow for 1 second difference due to precision/rounding
                    anomalies['retrograde_modifications'].append({
                        'file': file_path,
                        'mtime': datetime.fromtimestamp(mtime).isoformat(),
                        'ctime': datetime.fromtimestamp(ctime).isoformat()
                    })

            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred with '{file_path}': {e}")

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for temporal anomalies in file metadata."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--future-threshold",
        type=int,
        default=60,
        help="Number of seconds into the future a timestamp can be before being flagged. Default: 60."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for temporal anomalies...")
    results = find_temporal_anomalies(args.path, args.future_threshold)

    if not results['future_timestamps'] and not results['retrograde_modifications']:
        print("No temporal anomalies detected. All clear!")
    else:
        if results['future_timestamps']:
            print("\n--- Future Timestamps Detected ---")
            for anomaly in results['future_timestamps']:
                print(f"  File: {anomaly['file']}")
                print(f"    Type: {anomaly['type']}")
                print(f"    Timestamp: {anomaly.get('mtime') or anomaly.get('ctime')}")
                print(f"    Current Time: {anomaly['current_time']}")
        if results['retrograde_modifications']:
            print("\n--- Retrograde Modifications Detected ---")
            for anomaly in results['retrograde_modifications']:
                print(f"  File: {anomaly['file']}")
                print(f"    mtime: {anomaly['mtime']}")
                print(f"    ctime: {anomaly['ctime']}")
    print("\nScan complete.")

if __name__ == "__main__":
    main()
