import os
import sys
import time
from datetime import datetime, timedelta

def is_empty_dir(path):
    """Checks if a directory is empty (contains no files or subdirectories)."""
    # Mock rationale: os.listdir is mocked in tests to simulate directory contents.
    return not os.listdir(path)

def is_old_file(filepath, age_threshold_days):
    """Checks if a file is older than the specified age threshold."""
    if not os.path.isfile(filepath):
        return False
    # Mock rationale: os.path.getmtime is mocked in tests to control file modification times.
    # datetime.now is mocked to control the 'current' time for age calculation.
    file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
    current_time = datetime.now()
    return (current_time - file_mtime) > timedelta(days=age_threshold_days)

def matches_pattern(filename, patterns):
    """Checks if a filename matches any of the given patterns (extensions or suffixes)."""
    # Mock rationale: This function is pure and doesn't require mocking.
    for pattern in patterns:
        if filename.endswith(pattern):
            return True
    return False

def scan_for_dust_bunnies(target_dir, age_threshold_days=30, file_patterns=None):
    """
    Scans the target directory for empty folders and old/temporary files.

    Args:
        target_dir (str): The path to the directory to scan.
        age_threshold_days (int): Files older than this many days are considered old.
        file_patterns (list): List of file extensions/suffixes to consider as temporary.

    Returns:
        tuple: (list of empty_dirs, list of old_temp_files)
    """
    if file_patterns is None:
        file_patterns = ['.log', '.tmp', '~']

    empty_dirs = []
    old_temp_files = []

    # Mock rationale: os.walk is mocked in tests to simulate directory structure.
    for root, dirs, files in os.walk(target_dir):
        # Check for empty directories
        if not dirs and not files:
            empty_dirs.append(root)

        # Check for old/temporary files
        for file in files:
            filepath = os.path.join(root, file)
            if matches_pattern(file, file_patterns):
                if is_old_file(filepath, age_threshold_days):
                    old_temp_files.append((filepath, datetime.fromtimestamp(os.path.getmtime(filepath))))

    return empty_dirs, old_temp_files

def main():
    if len(sys.argv) < 2:
        print("Usage: python dust_bunny_sweeper.py <target_directory> [--age <days>] [--patterns <pattern1,pattern2,...>]")
        sys.exit(1)

    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        sys.exit(1)

    age_threshold_days = 30
    file_patterns = ['.log', '.tmp', '~']

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--age' and i + 1 < len(sys.argv):
            try:
                age_threshold_days = int(sys.argv[i+1])
                i += 1
            except ValueError:
                print("Error: --age must be an integer.")
                sys.exit(1)
        elif arg == '--patterns' and i + 1 < len(sys.argv):
            file_patterns = sys.argv[i+1].split(',')
            i += 1
        i += 1

    print("\n🧹🐰 Digital Dust Bunny Sweeper Report 🐰🧹")
    print(f"\nScanning: {target_dir}")
    print(f"Age Threshold: {age_threshold_days} days")
    print(f"File Patterns: {file_patterns}")
    print("\n" + "-" * 20)

    empty_dirs, old_temp_files = scan_for_dust_bunnies(target_dir, age_threshold_days, file_patterns)

    if empty_dirs:
        print("\n--- Empty Directories ---")
        for d in empty_dirs:
            print(f"- {d}")
    else:
        print("\n--- No Empty Directories Found ---")

    if old_temp_files:
        print("\n--- Old/Temporary Files ---")
        for f, mtime in old_temp_files:
            print(f"- {f} (Last modified: {mtime.strftime('%Y-%m-%d')})")
    else:
        print("\n--- No Old/Temporary Files Found ---")

    total_found = len(empty_dirs) + len(old_temp_files)
    print("\n" + "-" * 20)
    if total_found > 0:
        print(f"Found {total_found} digital dust bunnies. Consider giving them a good sweep!")
    else:
        print("Your digital space is sparkling clean! No dust bunnies found.")
    print("--- Scan Complete! ---")

if __name__ == "__main__":
    main()
