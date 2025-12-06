import os
import time
import argparse
import fnmatch
from datetime import datetime, timedelta

def find_forgotten_files(root_path, age_days, patterns=None, verbose=False):
    """
    Scans a directory for files older than a specified age and matching optional patterns.

    Args:
        root_path (str): The root directory to start scanning from.
        age_days (int): Files older than this many days will be considered 'forgotten'.
        patterns (list, optional): A list of glob patterns to filter files (e.g., ['*.log', '*.tmp']).
                                   If None, all files are considered.
        verbose (bool): If True, print detailed information during scanning.

    Returns:
        list: A list of full paths to forgotten files.
    """
    if not os.path.isdir(root_path):
        print(f"Error: Path '{root_path}' is not a valid directory.")
        return []

    forgotten_files = []
    cutoff_timestamp = (datetime.now() - timedelta(days=age_days)).timestamp()

    if verbose:
        print(f"Foraging for files older than {age_days} days (before {datetime.fromtimestamp(cutoff_timestamp).strftime('%Y-%m-%d %H:%M:%S')}) in '{root_path}'...")
        if patterns:
            print(f"Filtering by patterns: {', '.join(patterns)}")

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            try:
                # Skip if it's not a file (e.g., broken symlink, special file)
                if not os.path.isfile(full_path):
                    if verbose: print(f"Skipping non-file: {full_path}")
                    continue

                mod_time = os.path.getmtime(full_path)
                if mod_time < cutoff_timestamp:
                    # Check patterns if provided
                    if patterns:
                        matched = False
                        for pattern in patterns:
                            # Handle patterns like '__pycache__/*' by checking dirpath + filename
                            # or just filename depending on pattern type
                            if '/' in pattern or '\\' in pattern:
                                # Pattern includes path separators, match against relative path from root_path
                                relative_path = os.path.relpath(full_path, root_path)
                                if fnmatch.fnmatch(relative_path, pattern):
                                    matched = True
                                    break
                            else:
                                # Pattern is just for filename
                                if fnmatch.fnmatch(filename, pattern):
                                    matched = True
                                    break
                        if not matched:
                            if verbose: print(f"Skipping {full_path} (no pattern match)")
                            continue

                    forgotten_files.append(full_path)
                    if verbose:
                        print(f"Found forgotten file: {full_path} (Modified: {datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')})")
                elif verbose:
                    print(f"Skipping {full_path} (too new)")
            except OSError as e:
                if verbose: print(f"Error accessing {full_path}: {e}")
            except Exception as e:
                if verbose: print(f"Unexpected error with {full_path}: {e}")

    return forgotten_files

def delete_files(file_list, verbose=False):
    """
    Deletes a list of files.

    Args:
        file_list (list): A list of full paths to files to delete.
        verbose (bool): If True, print each file being deleted.
    """
    if not file_list:
        if verbose: print("No files to delete.")
        return

    print(f"Attempting to delete {len(file_list)} files...")
    for f_path in file_list:
        try:
            os.remove(f_path)
            if verbose: print(f"Successfully deleted: {f_path}")
        except OSError as e:
            print(f"Error deleting {f_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Forgotten File Forager: Unearths and optionally cleans up old, neglected files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start foraging from."
    )
    parser.add_argument(
        "--age",
        type=int,
        required=True,
        help="Files older than this many days will be considered 'forgotten'."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        help="Comma-separated list of glob patterns (e.g., '*.log,__pycache__/*') to filter files."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="If present, the forager will actually delete the identified forgotten files. Use with caution!"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about files being processed."
    )

    args = parser.parse_args()

    patterns_list = [p.strip() for p in args.patterns.split(',')] if args.patterns else None

    forgotten_files = find_forgotten_files(
        args.path, args.age, patterns_list, args.verbose
    )

    if forgotten_files:
        print(f"\nFound {len(forgotten_files)} forgotten files:")
        for f in forgotten_files:
            print(f"  - {f}")

        if args.delete:
            confirm = input("\nAre you sure you want to delete these files? (yes/no): ")
            if confirm.lower() == 'yes':
                delete_files(forgotten_files, args.verbose)
                print("Deletion complete.")
            else:
                print("Deletion cancelled by user.")
        else:
            print("\nRun with --delete to remove these files.")
    else:
        print("No forgotten files found matching criteria.")

if __name__ == "__main__":
    main()
