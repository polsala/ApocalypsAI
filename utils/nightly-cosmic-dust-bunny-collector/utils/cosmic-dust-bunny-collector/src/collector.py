import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Returns the age of a file in days."""
    mtime = os.path.getmtime(filepath)
    return (time.time() - mtime) / (60 * 60 * 24)

def is_file_old(filepath, max_age_days):
    """Checks if a file is older than max_age_days."""
    if not os.path.isfile(filepath):
        return False
    return get_file_age_days(filepath) > max_age_days

def is_file_empty(filepath):
    """Checks if a file is empty."""
    if not os.path.isfile(filepath):
        return False
    return os.path.getsize(filepath) == 0

def matches_pattern(filename, patterns):
    """Checks if a filename matches any of the given patterns (simple glob-like)."""
    if not patterns:
        return False
    for pattern in patterns:
        if pattern.startswith('*') and filename.endswith(pattern[1:]):
            return True
        if pattern.endswith('*') and filename.startswith(pattern[:-1]):
            return True
        if pattern == filename:
            return True
    return False

def scan_directory(directory, max_age_days=None, include_empty=False, patterns=None):
    """
    Scans a directory for 'dust bunny' files based on criteria.
    Returns a dictionary of categories with lists of file paths.
    """
    dust_bunnies = {
        "old_files": [],
        "empty_files": [],
        "pattern_matches": []
    }

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return dust_bunnies

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            if max_age_days is not None and is_file_old(filepath, max_age_days):
                dust_bunnies["old_files"].append(filepath)

            if include_empty and is_file_empty(filepath):
                dust_bunnies["empty_files"].append(filepath)

            if patterns and matches_pattern(filename, patterns):
                dust_bunnies["pattern_matches"].append(filepath)
    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Tidy up your digital space by finding old, empty, or temporary files."
    )
    parser.add_argument("directory", help="The directory to scan for dust bunnies.")
    parser.add_argument(
        "--max-age",
        type=int,
        default=30,
        help="Files older than this many days will be flagged as 'old'. Default: 30 days."
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Flag empty files as dust bunnies."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        help="Space-separated list of file patterns (e.g., '*.tmp', 'backup.log'). Supports simple glob-like matching with * at start/end."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for cosmic dust bunnies...")
    results = scan_directory(
        args.directory,
        max_age_days=args.max_age,
        include_empty=args.include_empty,
        patterns=args.patterns
    )

    found_any = False
    if results["old_files"]:
        print("\n--- Ancient Artifacts (Older than {} days) ---".format(args.max_age))
        for f in results["old_files"]:
            print(f"- {f}")
        found_any = True

    if results["empty_files"]:
        print("\n--- Void Voids (Empty Files) ---")
        for f in results["empty_files"]:
            print(f"- {f}")
        found_any = True

    if results["pattern_matches"]:
        print("\n--- Transient Traces (Matching Patterns: {}) ---".format(", ".join(args.patterns)))
        for f in results["pattern_matches"]:
            print(f"- {f}")
        found_any = True

    if not found_any:
        print("\n✨ All clear! No cosmic dust bunnies found in your quadrant. Your digital space is pristine! ✨")
    else:
        print("\n🧹 Time to sweep! Consider reviewing these files for potential cleanup. 🧹")

if __name__ == "__main__":
    main()
