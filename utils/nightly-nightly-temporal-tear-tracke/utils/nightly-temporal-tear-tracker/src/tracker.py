import os
import argparse
from datetime import datetime, timedelta

def find_stale_files(root_path: str, age_days: int) -> list[tuple[str, datetime]]:
    """
    Scans a directory for files not modified within the specified age.

    Args:
        root_path: The path to the directory to scan.
        age_days: The minimum number of days since last modification for a file to be considered stale.

    Returns:
        A list of tuples, where each tuple contains (file_path, last_modified_datetime).
    """
    stale_files = []
    now = datetime.now()
    threshold_date = now - timedelta(days=age_days)

    if not os.path.isdir(root_path):
        print(f"Error: Directory not found at '{root_path}'")
        return []

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                # Get modification time in seconds since the epoch
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < threshold_date:
                    stale_files.append((file_path, mod_datetime))
            except OSError as e:
                print(f"Warning: Could not access file '{file_path}': {e}")
                continue
    return stale_files

def main():
    parser = argparse.ArgumentParser(
        description="Identify files not modified within a specified period (Temporal Tears)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for stale files."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="The minimum number of days since last modification for a file to be considered stale."
    )

    args = parser.parse_args()

    if args.age < 0:
        print("Error: --age must be a non-negative integer.")
        exit(1)

    print(f"Scanning '{args.path}' for files not modified in {args.age} days...")
    stale_files = find_stale_files(args.path, args.age)

    if stale_files:
        print("\nTemporal Tears (files not modified in {} days):".format(args.age))
        for file_path, mod_date in stale_files:
            print(f"{file_path} (Last Modified: {mod_date.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print(f"\nNo temporal tears found in '{args.path}' older than {args.age} days. All clear!")

if __name__ == "__main__":
    main()
