import os
import time
import argparse
from datetime import datetime, timedelta

def find_dust_bunnies(path, age_threshold_days=90, file_extensions=None):
    """
    Scans the given path for empty directories and old files.

    Args:
        path (str): The root directory to scan.
        age_threshold_days (int): Files older than this many days are considered 'old'.
        file_extensions (list): List of file extensions to consider for age-based cleanup.
                                If None, a default set of common temporary extensions is used.

    Returns:
        dict: A dictionary containing lists of 'empty_dirs' and 'old_files'.
    """
    empty_dirs = []
    old_files = []
    now = datetime.now()
    age_threshold_timestamp = (now - timedelta(days=age_threshold_days)).timestamp()

    if file_extensions is None:
        file_extensions = ['.log', '.tmp', '.bak', '.old', '.temp', '.cache']

    for dirpath, dirnames, filenames in os.walk(path):
        # Check for empty directories
        if not dirnames and not filenames and os.path.isdir(dirpath):
            empty_dirs.append(dirpath)

        # Check for old files with specified extensions
        for filename in filenames:
            if any(filename.endswith(ext) for ext in file_extensions):
                filepath = os.path.join(dirpath, filename)
                try:
                    # Use os.path.getmtime for last modification time
                    # This is mocked in tests for determinism
                    mod_time = os.path.getmtime(filepath)
                    if mod_time < age_threshold_timestamp:
                        old_files.append((filepath, datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')))
                except OSError: # File might have been deleted during scan, or permissions issue
                    continue

    return {
        'empty_dirs': empty_dirs,
        'old_files': old_files
    }

def generate_report(dust_bunnies, target_path):
    """
    Generates a whimsical report of the found dust bunnies.

    Args:
        dust_bunnies (dict): The dictionary of found dust bunnies.
        target_path (str): The path that was scanned.

    Returns:
        str: The formatted report string.
    """
    report = []
    report.append(f"✨ Initiating Cosmic Debris Scan for: {target_path} ✨\n")
    report.append("Scanning the astral plains of your filesystem...\n")
    report.append("--- Cosmic Debris Report ---\n")

    if dust_bunnies['empty_dirs']:
        report.append("🌌 Empty Voids Discovered (Empty Directories):\n")
        for d in dust_bunnies['empty_dirs']:
            report.append(f"  - {d}\n")
    else:
        report.append("🌌 No Empty Voids detected. Your space is efficiently utilized!\n")

    report.append("\n") # Spacer

    if dust_bunnies['old_files']:
        report.append("⏳ Ancient Relics Unearthed (Old Files):\n")
        for f, date_str in dust_bunnies['old_files']:
            report.append(f"  - {f} (Last modified: {date_str})\n")
    else:
        report.append("⏳ No Ancient Relics found. Your files are spry and current!\n")

    report.append("\n--- End of Report ---\n")
    report.append("🧹 A clean sweep for your cosmic data-verse! 🧹\n")

    return "".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Whimsically cleans your digital space."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The absolute or relative path to the directory to scan.'
    )
    parser.add_argument(
        '--age-days', 
        type=int, 
        default=90, 
        help='Files older than this many days will be flagged. Default is 90.'
    )
    parser.add_argument(
        '--extensions', 
        nargs='*', 
        default=None, 
        help='Space-separated list of file extensions to consider (e.g., .log .tmp).'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The specified path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{args.path}' for digital dust bunnies...")
    dust_bunnies = find_dust_bunnies(args.path, args.age_days, args.extensions)
    report = generate_report(dust_bunnies, args.path)
    print(report)

if __name__ == '__main__':
    main()
