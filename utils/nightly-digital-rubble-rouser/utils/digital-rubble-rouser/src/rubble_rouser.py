import os
import argparse
from datetime import datetime, timedelta

def get_file_info(filepath):
    """Returns (size_mb, last_modified_dt) for a given file, or (None, None) on error."""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        mtime_timestamp = os.path.getmtime(filepath)
        last_modified_dt = datetime.fromtimestamp(mtime_timestamp)
        return size_mb, last_modified_dt
    except OSError:
        return None, None

def find_rubble(directory, max_age_days=None, min_size_mb=None, recursive=False):
    """
    Scans a directory for files matching age and size criteria.
    Returns a list of (filepath, size_mb, last_modified_dt) tuples.
    """
    rubble_files = []
    now = datetime.now()

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            size_mb, last_modified_dt = get_file_info(filepath)

            if size_mb is None: # Skip if file info couldn't be retrieved (e.g., permission error)
                continue

            is_old = False
            if max_age_days is not None:
                age_limit = now - timedelta(days=max_age_days)
                if last_modified_dt < age_limit:
                    is_old = True

            is_large = False
            if min_size_mb is not None:
                if size_mb >= min_size_mb:
                    is_large = True

            # A file is "rubble" if it meets all specified criteria.
            # If a criterion is not specified (e.g., max_age_days is None), it's considered met.
            # At least one criterion must have been specified in the first place (handled by main).
            if (max_age_days is None or is_old) and \
               (min_size_mb is None or is_large):
                rubble_files.append((filepath, size_mb, last_modified_dt))
        
        if not recursive:
            break # Only process the top directory if not recursive
            
    return rubble_files

def main():
    parser = argparse.ArgumentParser(
        description="Digital Rubble Rouser: Identify old or large files to clean up digital debris."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The directory path to scan for digital rubble."
    )
    parser.add_argument(
        "--age",
        type=int,
        help="List files older than this many days."
    )
    parser.add_argument(
        "--size",
        type=float,
        help="List files larger than this many megabytes (MB)."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan subdirectories recursively."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' not found.")
        exit(1)

    if args.age is None and args.size is None:
        print("Error: Please specify at least one criterion: --age or --size.")
        parser.print_help()
        exit(1)

    print(f"Scanning '{args.path}' for digital rubble...")
    rubble = find_rubble(args.path, args.age, args.size, args.recursive)

    if not rubble:
        print("No digital rubble found matching your criteria. Your digital space is pristine!")
        exit(0)

    print("\n--- Identified Digital Rubble ---")
    for filepath, size_mb, last_modified_dt in rubble:
        print(f"  Path: {filepath}")
        print(f"    Size: {size_mb:.2f} MB")
        print(f"    Last Modified: {last_modified_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 30)
    
    print(f"\nFound {len(rubble)} pieces of digital rubble.")
    print("Consider reviewing these files for potential cleanup.")

if __name__ == "__main__":
    main()
