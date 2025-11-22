import os
import argparse
from datetime import datetime, timedelta

def find_stale_files(root_dir: str, stale_days: int) -> list[tuple[str, datetime]]:
    """
    Scans a directory for files not modified within the last 'stale_days'.

    Args:
        root_dir: The path to the directory to scan.
        stale_days: The number of days after which a file is considered stale.

    Returns:
        A list of tuples, where each tuple contains the path to a stale file
        and its last modification datetime.
    """
    stale_files = []
    now = datetime.now()
    stale_threshold = now - timedelta(days=stale_days)

    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found at '{root_dir}'")
        return []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < stale_threshold:
                    stale_files.append((file_path, mod_datetime))
            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}")
                continue
    return stale_files

def main():
    parser = argparse.ArgumentParser(
        description="Detects files not modified within a specified number of days."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="The number of days after which a file is considered 'stale' if not modified. (Default: 90)"
    )

    args = parser.parse_args()

    print(f"Scanning {args.path} for files not modified in {args.days} days...\n")

    stale_files = find_stale_files(args.path, args.days)

    if stale_files:
        print("Temporal Anomalies Detected:")
        for file_path, mod_datetime in stale_files:
            print(f"- {file_path} (Last Modified: {mod_datetime.strftime('%Y-%m-%d %H:%M:%S')})")
        print("\nConsider reviewing, archiving, or deleting these files to maintain a lean and efficient project.")
    else:
        print("No temporal anomalies detected. Your project is spick and span!")

if __name__ == "__main__":
    main()
