import os
import datetime
import time

def find_temporal_anomalies(
    path: str,
    future_threshold_days: int = 1,
    past_modified_threshold_days: int = 365,
    recent_modification_window_days: int = 7
) -> dict:
    """
    Scans a directory for files with unusual modification timestamps.

    Args:
        path: The directory to scan.
        future_threshold_days: Files modified more than this many days in the future
                               are considered anomalies.
        past_modified_threshold_days: Files older than this many days, but modified
                                      within recent_modification_window_days, are
                                      considered anomalies.
        recent_modification_window_days: The window to check for recent modifications
                                         for old files.

    Returns:
        A dictionary containing lists of 'future_anomalies' and 'past_modified_anomalies'.
    """
    anomalies = {
        "future_anomalies": [],
        "past_modified_anomalies": []
    }
    current_timestamp = time.time()
    future_threshold_timestamp = current_timestamp + (future_threshold_days * 24 * 3600)
    past_modified_check_timestamp = current_timestamp - (recent_modification_window_days * 24 * 3600)

    for root, _, files in os.walk(path):
        for file_name in files:
            full_path = os.path.join(root, file_name)
            try:
                mtime = os.path.getmtime(full_path)
                ctime = os.path.getctime(full_path) # Creation time might also be useful, but mtime is more direct for "modification"
                
                # Check for future anomalies
                if mtime > future_threshold_timestamp:
                    anomalies["future_anomalies"].append({
                        "path": full_path,
                        "mtime": datetime.datetime.fromtimestamp(mtime).isoformat(),
                        "reason": f"Modification time is {round((mtime - current_timestamp) / (24 * 3600))} days in the future."
                    })
                
                # Check for old files recently modified
                # A file is "old" if its creation time is significantly in the past
                # And it's "recently modified" if its modification time is within the recent window
                if ctime < (current_timestamp - (past_modified_threshold_days * 24 * 3600)) and \
                   mtime > past_modified_check_timestamp:
                    anomalies["past_modified_anomalies"].append({
                        "path": full_path,
                        "mtime": datetime.datetime.fromtimestamp(mtime).isoformat(),
                        "ctime": datetime.datetime.fromtimestamp(ctime).isoformat(),
                        "reason": f"File created over {past_modified_threshold_days} days ago, but modified within the last {recent_modification_window_days} days."
                    })

            except OSError as e:
                # Handle cases where file might be inaccessible or deleted during scan
                print(f"Warning: Could not access {full_path}: {e}")
                continue
    return anomalies

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Detect temporal anomalies in file modification times.")
    parser.add_argument("path", type=str, help="The directory to scan.")
    parser.add_argument("--future-days", type=int, default=1,
                        help="Threshold in days for future modification times.")
    parser.add_argument("--old-modified-days", type=int, default=365,
                        help="Threshold in days for considering a file 'old' by creation time.")
    parser.add_argument("--recent-window-days", type=int, default=7,
                        help="Window in days for 'recent modification' of old files.")

    args = parser.parse_args()

    results = find_temporal_anomalies(
        args.path,
        future_threshold_days=args.future_days,
        past_modified_threshold_days=args.old_modified_days,
        recent_modification_window_days=args.recent_window_days
    )

    print(json.dumps(results, indent=2))
