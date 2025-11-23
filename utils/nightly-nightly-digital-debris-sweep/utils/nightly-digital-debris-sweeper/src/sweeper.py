import os
import argparse
import datetime
import time
import fnmatch

def get_file_age_days(filepath):
    """Calculates the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (24 * 3600)
    except OSError:
        return -1 # Indicate error or non-existent file

def scan_directory(directory, age_threshold_days=0, patterns=None):
    """
    Scans a directory for files that are older than a threshold or match specific patterns.

    Args:
        directory (str): The path to the directory to scan.
        age_threshold_days (int): Files older than this many days will be considered debris.
                                  Set to 0 to disable age-based filtering.
        patterns (list[str]): A list of glob-style patterns (e.g., ['*.tmp', '*.log.old']).
                              Files matching any pattern will be considered debris.
                              Set to None or empty list to disable pattern-based filtering.

    Returns:
        list[str]: A list of file paths identified as digital debris.
    """
    debris_files = []
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found or is not a directory.")
        return []

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            is_debris = False

            # Check by age
            if age_threshold_days > 0:
                age = get_file_age_days(filepath)
                if age > age_threshold_days:
                    is_debris = True

            # Check by pattern
            if not is_debris and patterns: # Only check patterns if not already marked as debris
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        is_debris = True
                        break

            if is_debris:
                debris_files.append(filepath)
    return debris_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Digital Debris Sweeper: Scans directories for old or temporary files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan for debris."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered debris (default: 30). Set to 0 to disable."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        default="*.tmp,*.bak,*.log.old",
        help="Comma-separated glob patterns for files to consider debris (e.g., '*.tmp,*.log'). Set to empty string to disable."
    )

    args = parser.parse_args()

    patterns_list = [p.strip() for p in args.patterns.split(',') if p.strip()] if args.patterns else []

    print(f"Scanning '{args.directory}' for digital debris...")
    print(f"  - Files older than: {args.age} days")
    print(f"  - Files matching patterns: {', '.join(patterns_list) if patterns_list else 'None'}")
    print("-" * 40)

    debris = scan_directory(args.directory, args.age, patterns_list)

    if debris:
        print("\nIdentified Digital Debris:")
        for item in debris:
            print(f"  - {item}")
        print(f"\nTotal debris found: {len(debris)} files.")
        print("Consider reviewing and removing these files to tidy up your digital landscape.")
    else:
        print("\nNo digital debris found. Your digital landscape is pristine!")

if __name__ == "__main__":
    main()
