import os
import shutil
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        modified_date = datetime.fromtimestamp(mtime)
        return (datetime.now() - modified_date).days
    except OSError:
        return -1 # Indicate error or file not found

def find_data_debris(paths, age_threshold_days):
    """
    Scans specified directories for files older than age_threshold_days.
    Returns a list of paths to identified debris files.
    """
    debris_files = []
    print(f"🔍 Initiating scan for data debris older than {age_threshold_days} days...")
    for path in paths:
        if not os.path.isdir(path):
            print(f"⚠️ Warning: Path '{path}' is not a valid directory. Skipping.")
            continue

        print(f"Scanning '{path}' for ancient digital relics...")
        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                age = get_file_age_days(filepath)
                if age >= age_threshold_days:
                    debris_files.append(filepath)
    return debris_files

def report_debris(debris_files):
    """Reports the identified data debris."""
    if not debris_files:
        print("\n✨ All clear! No significant data debris detected. Your digital wasteland is surprisingly tidy.")
        return

    print(f"\n🚨 Attention, Scavenger! {len(debris_files)} pieces of data debris detected:")
    for file in debris_files:
        print(f"  - {file} (Age: {get_file_age_days(file)} days)")
    print("\nConsider your next move: quarantine or dust?")

def quarantine_debris(debris_files, quarantine_dir):
    """Moves identified data debris to a quarantine directory."""
    if not debris_files:
        print("\n✨ No data debris to quarantine. The digital winds are calm.")
        return

    os.makedirs(quarantine_dir, exist_ok=True)
    print(f"\n📦 Initiating Quarantine Protocol for {len(debris_files)} items to '{quarantine_dir}'...")
    moved_count = 0
    for file_path in debris_files:
        try:
            # Preserve directory structure within quarantine
            # This assumes a common root for all debris files for simplicity in relative path calculation
            # For more complex scenarios, a different strategy might be needed (e.g., timestamped subfolders).
            common_root = os.path.commonpath(debris_files) if debris_files else ''
            relative_path = os.path.relpath(file_path, start=common_root)
            destination_path = os.path.join(quarantine_dir, relative_path)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.move(file_path, destination_path)
            print(f"  - Moved '{file_path}' to '{destination_path}'")
            moved_count += 1
        except Exception as e:
            print(f"  - Failed to quarantine '{file_path}': {e}")
    print(f"\n✅ Quarantine complete. {moved_count} items safely contained. Review them at your leisure.")

def dust_debris(debris_files):
    """Permanently deletes identified data debris."""
    if not debris_files:
        print("\n✨ No data debris to dust. Your digital path is clear.")
        return

    print(f"\n🔥 Activating Dusting Protocol for {len(debris_files)} items. This is irreversible!")
    deleted_count = 0
    for file_path in debris_files:
        try:
            os.remove(file_path)
            print(f"  - Dusted '{file_path}' into oblivion.")
            deleted_count += 1
        except Exception as e:
            print(f"  - Failed to dust '{file_path}': {e}")
    print(f"\n💀 Dusting complete. {deleted_count} items permanently removed. May they rest in digital peace.")

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical utility to clear out old, unused files (data debris)."
    )
    parser.add_argument(
        "--path",
        nargs="+",
        required=True,
        help="One or more directories to scan for data debris."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="Files older than this many days will be considered debris (default: 90)."
    )
    parser.add_argument(
        "--mode",
        choices=["report", "quarantine", "dust"],
        default="report",
        help="Operation mode: 'report' (default), 'quarantine', or 'dust'."
    )
    parser.add_argument(
        "--quarantine-dir",
        help="Directory to move files to when in 'quarantine' mode. Required for 'quarantine' mode."
    )

    args = parser.parse_args()

    if args.mode == "quarantine" and not args.quarantine_dir:
        parser.error("--quarantine-dir is required when --mode is 'quarantine'.")

    debris_files = find_data_debris(args.path, args.age)

    if args.mode == "report":
        report_debris(debris_files)
    elif args.mode == "quarantine":
        quarantine_debris(debris_files, args.quarantine_dir)
    elif args.mode == "dust":
        dust_debris(debris_files)

if __name__ == "__main__":
    main()
