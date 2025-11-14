import os
import time
import argparse
from datetime import datetime, timedelta

def find_temporal_anomalies(
    directory_path: str,
    max_age_days: int = 30,
    min_age_seconds: int = 60
) -> list[dict]:
    """
    Scans a directory for files that are either too old or too new.

    Args:
        directory_path: The path to the directory to scan.
        max_age_days: Files older than this many days are considered 'TOO_OLD'.
        min_age_seconds: Files newer than this many seconds are considered 'TOO_NEW'.

    Returns:
        A list of dictionaries, each representing an anomaly with 'path', 'type', and 'mtime'.
    """
    anomalies = []
    now = datetime.now() # Mock rationale: datetime.now() is mocked in tests for determinism.

    # Calculate thresholds
    old_threshold = now - timedelta(days=max_age_days)
    new_threshold = now - timedelta(seconds=min_age_seconds)

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found: {directory_path}")
        return []

    for root, _, files in os.walk(directory_path): # Mock rationale: os.walk is mocked in tests to control file system traversal.
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                mtime_timestamp = os.path.getmtime(file_path) # Mock rationale: os.path.getmtime is mocked in tests to control file modification times.
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < old_threshold:
                    anomalies.append({
                        'path': file_path,
                        'type': 'TOO_OLD',
                        'mtime': mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    })
                elif mtime_datetime > new_threshold:
                    anomalies.append({
                        'path': file_path,
                        'type': 'TOO_NEW',
                        'mtime': mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    })
            except OSError as e:
                print(f"Warning: Could not access {file_path}: {e}")

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies (too old or too new files) in a directory."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=30,
        help="Files older than this many days are considered 'TOO_OLD'. Default: 30."
    )
    parser.add_argument(
        "--min-age-seconds",
        type=int,
        default=60,
        help="Files newer than this many seconds are considered 'TOO_NEW'. Default: 60."
    )

    args = parser.parse_args()

    print(f"Temporal Anomaly Report for: {args.directory_path}")
    print("-----------------------------------------")

    anomalies = find_temporal_anomalies(
        args.directory_path,
        args.max_age_days,
        args.min_age_seconds
    )

    if anomalies:
        for anomaly in anomalies:
            print(f"[{anomaly['type']}] {anomaly['path']} (Modified: {anomaly['mtime']})")
    else:
        print("No anomalies detected.")
    print("-----------------------------------------")

if __name__ == "__main__":
    main()
