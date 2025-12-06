import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_in_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        file_datetime = datetime.fromtimestamp(mtime)
        return (datetime.now() - file_datetime).days
    except OSError:
        return -1 # Indicate error or non-existent file

def hoover_directory(directory_path, age_threshold_days, delete_mode=False, verbose=False):
    """
    Scans a directory for files older than age_threshold_days and optionally deletes them.
    """
    if not os.path.isdir(directory_path):
        print(f"🚨 Error: Directory '{directory_path}' not found or is not a directory.")
        return

    print(f"\n🧹 Initiating Digital Dust Bunny Hoover in '{directory_path}'...")
    print(f"🔍 Searching for files older than {age_threshold_days} days...")
    if delete_mode:
        print("⚠️  DELETE MODE ACTIVATED! Files will be permanently removed. ⚠️")
    else:
        print("✅ Dry Run Mode: No files will be deleted. Use --delete to activate removal.")

    dust_bunnies_found = []
    total_size_freed = 0

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            age = get_file_age_in_days(filepath)

            if age >= age_threshold_days:
                try:
                    file_size = os.path.getsize(filepath)
                    dust_bunnies_found.append((filepath, age, file_size))
                    if verbose:
                        print(f"  [FOUND] '{filepath}' (Age: {age} days, Size: {file_size / (1024*1024):.2f} MB)")
                except OSError:
                    if verbose:
                        print(f"  [SKIPPED] '{filepath}' (Error getting info)")
                    continue

    if not dust_bunnies_found:
        print("\n🎉 No digital dust bunnies found! Your digital realm is pristine.")
        return

    print(f"\n--- 🐰 Digital Dust Bunnies Report ({len(dust_bunnies_found)} found) ---")
    for filepath, age, size in dust_bunnies_found:
        print(f"  - '{filepath}' (Age: {age} days, Size: {size / (1024*1024):.2f} MB)")
        total_size_freed += size

    print(f"\nTotal potential space to be purified: {total_size_freed / (1024*1024):.2f} MB")

    if delete_mode:
        print("\n--- 🗑️ Purifying Digital Realm ---")
        deleted_count = 0
        for filepath, _, _ in dust_bunnies_found:
            try:
                os.remove(filepath)
                print(f"  [DELETED] '{filepath}'")
                deleted_count += 1
            except OSError as e:
                print(f"  [FAILED TO DELETE] '{filepath}': {e}")
        print(f"\n✨ Purification complete! {deleted_count} files removed.")
    else:
        print("\nTo proceed with purification, run again with the '--delete' flag.")

    print("\n🧹 Digital Dust Bunny Hoover complete. May your bytes be ever free! 🧹")


def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Hoover: Whimsically purges old files from directories."
    )
    parser.add_argument("directory_path", type=str,
                        help="The root directory to start scanning from.")
    parser.add_argument("--age", type=int, required=True,
                        help="Files older than this many days will be considered dust bunnies.")
    parser.add_argument("--delete", action="store_true",
                        help="WARNING! Use this flag to actually delete the identified files.")
    parser.add_argument("--verbose", action="store_true",
                        help="Print detailed information about each file found.")

    args = parser.parse_args()

    hoover_directory(args.directory_path, args.age, args.delete, args.verbose)

if __name__ == "__main__":
    main()
