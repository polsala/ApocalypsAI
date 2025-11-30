import os
import sys
import argparse
from datetime import datetime, timedelta, timezone

def find_temporal_anomalies(
    directory_path: str,
    future_threshold_seconds: int = 5,
    ancient_year: int = 1980,
    recursive: bool = True
) -> list[dict]:
    """
    Scans a directory for files with temporal anomalies in their modification times.

    Args:
        directory_path: The path to the directory to scan.
        future_threshold_seconds: Number of seconds into the future a file's mtime
                                  can be before it's flagged.
        ancient_year: Files modified before this year will be flagged as ancient.
        recursive: If True, scan subdirectories; otherwise, only the top-level.

    Returns:
        A list of dictionaries, each describing an anomaly.
    """
    anomalies = []
    
    if not os.path.isdir(directory_path):
        # Error message printed by main function, or handled by caller
        return []

    current_time_utc = datetime.now(timezone.utc)
    future_limit_utc = current_time_utc + timedelta(seconds=future_threshold_seconds)
    ancient_limit_utc = datetime(ancient_year, 1, 1, tzinfo=timezone.utc)

    walk_iterator = os.walk(directory_path)
    if not recursive:
        # If not recursive, only iterate the first (root) directory
        # os.walk returns a generator, so we need to handle the case where it's empty
        try:
            walk_iterator = [next(walk_iterator)] 
        except StopIteration:
            return [] # Empty directory, nothing to scan

    for root, _, files in walk_iterator:
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                mtime_timestamp = os.path.getmtime(file_path)
                # Convert timestamp to UTC datetime for consistent comparison
                mtime_utc = datetime.fromtimestamp(mtime_timestamp, tz=timezone.utc)

                if mtime_utc > future_limit_utc:
                    anomalies.append({
                        "file": file_path,
                        "type": "FUTURE_MODIFICATION_TIME",
                        "mtime": mtime_utc.isoformat(),
                        "current_time": current_time_utc.isoformat(),
                        "details": f"Modified {mtime_utc.isoformat()} (future)"
                    })
                elif mtime_utc < ancient_limit_utc:
                    anomalies.append({
                        "file": file_path,
                        "type": "ANCIENT_MODIFICATION_TIME",
                        "mtime": mtime_utc.isoformat(),
                        "ancient_year_threshold": ancient_year,
                        "details": f"Modified {mtime_utc.isoformat()} (before {ancient_year})"
                    })
            except OSError as e:
                anomalies.append({
                    "file": file_path,
                    "type": "ACCESS_ERROR",
                    "details": f"Could not access file metadata: {e}"
                })
            except Exception as e:
                anomalies.append({
                    "file": file_path,
                    "type": "UNKNOWN_ERROR",
                    "details": f"An unexpected error occurred: {e}"
                })

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies in file modification times."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--future-threshold",
        type=int,
        default=5,
        help="Number of seconds into the future a file's mtime can be before it's flagged. Default: 5."
    )
    parser.add_argument(
        "--ancient-year",
        type=int,
        default=1980,
        help="Files modified before this year will be flagged as ancient. Default: 1980."
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="If set, the scanner will only check the top-level directory and not recurse into subdirectories."
    )

    args = parser.parse_args()

    anomalies = find_temporal_anomalies(
        args.directory_path,
        args.future_threshold,
        args.ancient_year,
        not args.no_recursive
    )

    if anomalies:
        print("Temporal Anomalies Detected:")
        for anomaly in anomalies:
            print(f"- File: {anomaly['file']}")
            print(f"  Type: {anomaly['type']}")
            print(f"  Details: {anomaly['details']}")
            print("-" * 20)
        sys.exit(1) # Indicate failure/anomalies found
    else:
        print(f"No temporal anomalies detected in '{args.directory_path}'. All clear!")
        sys.exit(0) # Indicate success/no anomalies

if __name__ == "__main__":
    main()
