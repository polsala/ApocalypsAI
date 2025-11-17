import os
import shutil
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime_timestamp = os.path.getmtime(filepath)
        mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
        age = datetime.now() - mtime_datetime
        return age.days
    except OSError:
        return -1 # Indicate an error or unreadable file

def find_debris_files(root_path, min_age_days):
    """
    Scans a directory for files older than min_age_days.
    Returns a list of file paths.
    """
    debris_files = []
    if not os.path.isdir(root_path):
        print(f"🚨 Warning: Path '{root_path}' is not a valid directory. No debris found here.")
        return debris_files

    print(f"🔍 Scanning '{root_path}' for data debris older than {min_age_days} days...")
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            age = get_file_age_in_days(filepath)
            if age >= min_age_days:
                debris_files.append(filepath)
    return debris_files

def quarantine_file(filepath, quarantine_dir_name="_quarantined_debris_"):
    """
    Moves a file to a quarantine subdirectory within its parent directory.
    Creates the quarantine directory if it doesn't exist.
    """
    parent_dir = os.path.dirname(filepath)
    quarantine_path = os.path.join(parent_dir, quarantine_dir_name)

    try:
        os.makedirs(quarantine_path, exist_ok=True)
        new_filepath = os.path.join(quarantine_path, os.path.basename(filepath))
        shutil.move(filepath, new_filepath)
        print(f"📦 Quarantined: '{filepath}' -> '{new_filepath}'")
        return True
    except OSError as e:
        print(f"❌ Failed to quarantine '{filepath}': {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Debris Duster: Identify and manage old, forgotten files."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The root directory to start scanning for debris."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="The minimum age in days for a file to be considered 'debris'."
    )
    parser.add_argument(
        "--mode",
        choices=["list", "quarantine"],
        required=True,
        help="Operation mode: 'list' to only print, 'quarantine' to move files."
    )
    parser.add_argument(
        "--quarantine-dir-name",
        default="_quarantined_debris_",
        help="Custom name for the quarantine subdirectory (default: '_quarantined_debris_')."
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"🚫 Error: The specified path '{args.path}' does not exist. Aborting duster operation.")
        exit(1)
    if not os.path.isdir(args.path):
        print(f"🚫 Error: The specified path '{args.path}' is not a directory. Aborting duster operation.")
        exit(1)
    if args.age < 0:
        print(f"🚫 Error: Age must be a non-negative integer. Got '{args.age}'. Aborting duster operation.")
        exit(1)

    debris_files = find_debris_files(args.path, args.age)

    if not debris_files:
        print(f"✨ All clear! No data debris older than {args.age} days found in '{args.path}'.")
        return

    print(f"\n--- Found {len(debris_files)} pieces of data debris ---")
    if args.mode == "list":
        for f in debris_files:
            print(f"🗑️  [DEBRIS] {f} (Age: {get_file_age_in_days(f)} days)")
        print("\n💡 Tip: Run with `--mode quarantine` to move these files to a quarantine zone.")
    elif args.mode == "quarantine":
        quarantined_count = 0
        for f in debris_files:
            if quarantine_file(f, args.quarantine_dir_name):
                quarantined_count += 1
        print(f"\n✅ Operation complete: {quarantined_count} files quarantined.")

if __name__ == "__main__":
    main()
