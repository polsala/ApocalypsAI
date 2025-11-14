import os
import time
import argparse
import fnmatch
from datetime import datetime

def find_dust_bunnies(path, age_days=30, patterns=None):
    """
    Scans a directory for empty directories and old files matching specified patterns.

    Args:
        path (str): The root directory to scan.
        age_days (int): Files older than this many days will be considered 'old'.
        patterns (list): List of glob patterns for files to check by age.

    Returns:
        dict: A dictionary containing lists of 'empty_dirs' and 'aged_files'.
    """
    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a valid directory.")

    if patterns is None:
        patterns = ['*.log', '*.tmp', 'temp_*']

    empty_dirs = []
    aged_files = []
    current_time = time.time()
    age_threshold = current_time - (age_days * 24 * 60 * 60)

    for root, dirs, files in os.walk(path):
        # Check for empty directories
        # A directory is considered empty if it has no subdirectories and no files.
        # The root path itself is generally not considered an 'empty directory' dust bunny.
        if not dirs and not files and root != path:
            empty_dirs.append(root)

        # Check for aged files
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Check if file matches any pattern
                is_match = False
                for pattern in patterns:
                    if fnmatch.fnmatch(file_name, pattern):
                        is_match = True
                        break
                
                if is_match:
                    mod_time = os.path.getmtime(file_path)
                    if mod_time < age_threshold:
                        aged_files.append({
                            'path': file_path,
                            'last_modified': datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
                        })
            except OSError: # Handle cases where file might be inaccessible or disappear during walk
                # Skip files that cause OS errors (e.g., permission denied, file deleted mid-scan)
                continue

    return {
        'empty_dirs': empty_dirs,
        'aged_files': aged_files
    }

def main():
    parser = argparse.ArgumentParser(
        description="Identify digital dust bunnies (empty directories, old temporary/log files).\n" +
                    "This utility reports findings and does NOT delete any files."
    )
    parser.add_argument('--path', type=str, required=True,
                        help='The root directory to scan for dust bunnies.')
    parser.add_argument('--age-days', type=int, default=30,
                        help='Minimum age in days for files to be considered old. Defaults to 30.')
    parser.add_argument('--patterns', nargs='*', default=['*.log', '*.tmp', 'temp_*'],
                        help='Space-separated glob patterns for files to check by age. Defaults to *.log *.tmp temp_*.')

    args = parser.parse_args()

    print(f"Scanning {args.path} for digital dust bunnies...\n")

    try:
        results = find_dust_bunnies(args.path, args.age_days, args.patterns)

        if results['empty_dirs']:
            print("--- Empty Directories ---")
            for d in results['empty_dirs']:
                print(f"- {d}")
            print()

        if results['aged_files']:
            print(f"--- Aged Files (older than {args.age_days} days) ---")
            for f in results['aged_files']:
                print(f"- {f['path']} (Last modified: {f['last_modified']})")
            print()

        if not results['empty_dirs'] and not results['aged_files']:
            print("No digital dust bunnies found. Your digital space is sparkling clean!")
        else:
            print("Sweeping complete! No actual sweeping performed, just reporting.")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
