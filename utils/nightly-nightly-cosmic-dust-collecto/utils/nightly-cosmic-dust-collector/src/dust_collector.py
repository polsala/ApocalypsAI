import os
import shutil
import time
import datetime
import argparse
import fnmatch

def collect_dust(path, age_days, action='report', destination=None, file_patterns=None):
    """
    Identifies and optionally acts upon old files ("cosmic dust") in a given directory.

    Args:
        path (str): The root directory to scan.
        age_days (int): Files older than this many days are considered dust.
        action (str): 'report' (default), 'delete', or 'move'.
        destination (str, optional): Required if action is 'move'. The directory to move files to.
        file_patterns (list, optional): A list of glob-style patterns (e.g., ['*.log', 'temp_*']).
                                        Only files matching these patterns will be considered.
                                        If None, all files are considered.

    Returns:
        list: A list of paths to the files identified as dust.
    """
    if action not in ['report', 'delete', 'move']:
        raise ValueError(f"Invalid action: {action}. Must be 'report', 'delete', or 'move'.")

    if action == 'move' and not destination:
        raise ValueError("Destination path is required for 'move' action.")
    
    if action == 'move' and destination:
        os.makedirs(destination, exist_ok=True) # Ensure destination exists

    dust_files = []
    current_timestamp = time.time()
    age_threshold_timestamp = current_timestamp - (age_days * 24 * 3600)

    print(f"Scanning '{path}' for files older than {age_days} days...")
    if file_patterns:
        print(f"Filtering by patterns: {', '.join(file_patterns)}")

    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)

            # Apply file pattern filter if specified
            if file_patterns:
                if not any(fnmatch.fnmatch(filename, pattern) for pattern in file_patterns):
                    continue # Skip if no pattern matches

            try:
                mod_time = os.path.getmtime(full_path)
                if mod_time < age_threshold_timestamp:
                    dust_files.append(full_path)
            except OSError as e:
                print(f"Warning: Could not access '{full_path}': {e}")
                continue

    print(f"Found {len(dust_files)} files identified as cosmic dust.")

    if action == 'report':
        if dust_files:
            print("\n--- Cosmic Dust Report ---")
            for f in dust_files:
                print(f"- {f}")
            print("--------------------------")
        else:
            print("No cosmic dust found. Your repository is sparkling clean!")
    elif action == 'delete':
        print("\n--- Deleting Cosmic Dust ---")
        for f in dust_files:
            try:
                os.remove(f)
                print(f"Deleted: {f}")
            except OSError as e:
                print(f"Error deleting '{f}': {e}")
        print("----------------------------")
    elif action == 'move':
        print(f"\n--- Moving Cosmic Dust to '{destination}' ---")
        for f in dust_files:
            try:
                # Construct destination path, preserving original filename
                dest_file_path = os.path.join(destination, os.path.basename(f))
                shutil.move(f, dest_file_path)
                print(f"Moved: {f} -> {dest_file_path}")
            except OSError as e:
                print(f"Error moving '{f}': {e}")
        print("---------------------------------------------")
    
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Sweeps away old files."
    )
    parser.add_argument(
        "path",
        help="The root directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files older than this many days will be considered cosmic dust (default: 30)."
    )
    parser.add_argument(
        "--action",
        choices=['report', 'delete', 'move'],
        default='report',
        help="Action to perform: 'report' (default), 'delete', or 'move'."
    )
    parser.add_argument(
        "--destination",
        help="Required if action is 'move'. The directory to move cosmic dust to."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        help="Optional glob-style file patterns (e.g., '*.log', 'temp_*'). Only files matching these will be considered."
    )

    args = parser.parse_args()

    try:
        collect_dust(
            args.path,
            args.age,
            args.action,
            args.destination,
            args.patterns
        )
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
