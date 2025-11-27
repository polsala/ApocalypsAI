import os
import time
import json
import argparse
from datetime import datetime, timedelta

def find_decayed_files(root_path: str, threshold_days: int, current_time: datetime = None) -> list:
    """
    Scans a directory for files whose most recent activity (modification or access)
    is older than the specified threshold.

    Args:
        root_path (str): The root directory to start scanning from.
        threshold_days (int): The number of days after which a file is
                              considered 'decayed'.
        current_time (datetime, optional): The current time to use for comparison.
                                           Defaults to datetime.now() if None.

    Returns:
        list: A list of dictionaries, each representing a decayed file
              with its path, last modified/accessed times, and age in days.
    """
    decayed_files = []
    if current_time is None:
        current_time = datetime.now()
    decay_cutoff = current_time - timedelta(days=threshold_days)

    if not os.path.isdir(root_path):
        return []

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Get modification and access times
                mtime_timestamp = os.path.getmtime(file_path)
                atime_timestamp = os.path.getatime(file_path)

                mtime = datetime.fromtimestamp(mtime_timestamp)
                atime = datetime.fromtimestamp(atime_timestamp)

                # A file is considered 'decayed' if its most recent activity
                # (max of mtime and atime) is older than the decay_cutoff.
                most_recent_activity = max(mtime, atime)
                if most_recent_activity < decay_cutoff:
                    age_days = (current_time - most_recent_activity).days
                    decayed_files.append({
                        "file": file_path,
                        "last_modified": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                        "last_accessed": atime.strftime("%Y-%m-%d %H:%M:%S"),
                        "age_days": age_days
                    })
            except OSError:
                # Handle cases where file might be inaccessible or deleted during scan
                pass # Suppress warnings for cleaner output, especially in tests
            except Exception:
                # Catch any other unexpected errors during file processing
                pass # Suppress warnings

    return decayed_files

def main():
    parser = argparse.ArgumentParser(
        description="Detects files that haven't been modified or accessed in a long time."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--threshold-days",
        type=int,
        default=90,
        help="The number of days after which a file is considered 'decayed'. (Default: 90)"
    )

    args = parser.parse_args()

    decayed_files = find_decayed_files(args.path, args.threshold_days)

    if decayed_files:
        print(json.dumps(decayed_files, indent=2))
    else:
        print(f"No decayed files found in '{args.path}' older than {args.threshold_days} days.")

if __name__ == "__main__":
    main()
