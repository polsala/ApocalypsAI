import os
import argparse
from datetime import datetime, timedelta

def scan_directory(root_path: str, threshold_days: int = 90) -> list[dict]:
    """
    Scans a directory for files older than a specified threshold.

    Args:
        root_path: The path to the directory to scan.
        threshold_days: The number of days a file must be untouched to be considered 'stale'.

    Returns:
        A list of dictionaries, each containing 'path', 'mtime', and 'age_days' for stale files.
    """
    if not os.path.isdir(root_path):
        raise FileNotFoundError(f"The specified path '{root_path}' is not a valid directory.")

    stale_files = []
    current_time = datetime.now()
    stale_cutoff = current_time - timedelta(days=threshold_days)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Get modification time as a datetime object
                mtime_timestamp = os.path.getmtime(file_path)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < stale_cutoff:
                    age_days = (current_time - mtime_datetime).days
                    stale_files.append({
                        'path': file_path,
                        'mtime': mtime_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                        'age_days': age_days
                    })
            except OSError as e:
                # Handle cases where file might be inaccessible or deleted during scan
                print(f"Warning: Could not access file '{file_path}': {e}")
                continue
    return stale_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Temporal Tear Tracker: Unearthing forgotten files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=90,
        help="The number of days a file must be untouched to be considered 'stale'. (Default: 90)"
    )

    args = parser.parse_args()

    try:
        print(f"\nScanning '{args.path}' for files older than {args.threshold} days...")
        stale_files = scan_directory(args.path, args.threshold)

        if stale_files:
            print("\n--- Temporal Tears Detected ---")
            for file_info in stale_files:
                print(f"  Path: {file_info['path']}")
                print(f"  Last Modified: {file_info['mtime']} ({file_info['age_days']} days ago)")
                print("  ----------------------------")
            print(f"\nTotal stale files found: {len(stale_files)}")
            print("Consider reviewing these relics of a bygone era.")
        else:
            print("\nNo temporal tears found. All files are fresh and vibrant!")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected anomaly occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
