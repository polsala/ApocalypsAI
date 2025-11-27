import os
import time
import argparse
from datetime import datetime, timedelta

def find_temporal_anomalies(
    root_dir: str,
    max_age_years: int = 5,
    future_tolerance_seconds: int = 60
) -> dict:
    """
    Scans a directory for files with temporal anomalies (future or ancient modification times).

    Args:
        root_dir: The root directory to start scanning.
        max_age_years: Files older than this many years will be flagged as "ancient".
        future_tolerance_seconds: Files modified more than this many seconds in the future
                                  will be flagged.

    Returns:
        A dictionary containing lists of 'future_files' and 'ancient_files'.
    """
    anomalies = {
        "future_files": [],
        "ancient_files": []
    }

    current_time_dt = datetime.now()
    current_timestamp = current_time_dt.timestamp()

    ancient_threshold_dt = current_time_dt - timedelta(days=max_age_years * 365) # Simple year calc
    ancient_threshold_timestamp = ancient_threshold_dt.timestamp()

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                # Get modification time (mtime)
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_dt = datetime.fromtimestamp(mtime_timestamp)

                # Check for future files
                if mtime_timestamp > (current_timestamp + future_tolerance_seconds):
                    anomalies["future_files"].append({
                        "path": filepath,
                        "mtime": mtime_dt.isoformat(),
                        "reason": f"Modified {round((mtime_timestamp - current_timestamp) / 60, 2)} minutes in the future"
                    })
                # Check for ancient files
                elif mtime_timestamp < ancient_threshold_timestamp:
                    anomalies["ancient_files"].append({
                        "path": filepath,
                        "mtime": mtime_dt.isoformat(),
                        "reason": f"Modified {max_age_years} years ago or more"
                    })
            except OSError as e:
                # Handle cases where file might be inaccessible or deleted during scan
                print(f"Warning: Could not access {filepath} - {e}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies in file modification times."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan for anomalies."
    )
    parser.add_argument(
        "--max-age-years",
        type=int,
        default=5,
        help="Files older than this many years will be flagged as 'ancient'. Default: 5"
    )
    parser.add_argument(
        "--future-tolerance-seconds",
        type=int,
        default=60,
        help="Files modified more than this many seconds in the future will be flagged. Default: 60"
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' does not exist or is not a directory.")
        exit(1)

    print(f"Scanning '{args.directory}' for temporal anomalies...")
    anomalies = find_temporal_anomalies(
        args.directory,
        args.max_age_years,
        args.future_tolerance_seconds
    )

    if anomalies["future_files"] or anomalies["ancient_files"]:
        print("\n--- Temporal Anomalies Detected ---")
        if anomalies["future_files"]:
            print("\nFuture Files:")
            for item in anomalies["future_files"]:
                print(f"  Path: {item['path']}")
                print(f"  MTime: {item['mtime']}")
                print(f"  Reason: {item['reason']}")
                print("-" * 20)
        if anomalies["ancient_files"]:
            print("\nAncient Files:")
            for item in anomalies["ancient_files"]:
                print(f"  Path: {item['path']}")
                print(f"  MTime: {item['mtime']}")
                print(f"  Reason: {item['reason']}")
                print("-" * 20)
    else:
        print("\nNo temporal anomalies detected. All timestamps appear to be in order!")

if __name__ == "__main__":
    main()
