import os
import datetime
import argparse
import fnmatch
import json

def is_excluded(filepath, exclude_patterns):
    """Checks if a file path matches any of the exclusion patterns."""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(filepath, pattern):
            return True
    return False

def collect_dust(path, age_days, exclude_patterns, current_time=None):
    """Collects files older than a specified age in days.

    Args:
        path (str): The root directory to scan.
        age_days (int): The minimum age in days for a file to be considered 'dusty'.
        exclude_patterns (list): A list of glob-style patterns to exclude files/directories.
        current_time (datetime.datetime, optional): The current time to use for comparison.
                                                    Defaults to datetime.datetime.now().

    Returns:
        list: A list of dictionaries, each containing 'path' and 'last_modified' for dusty files.
    """
    if current_time is None:
        current_time = datetime.datetime.now()

    dusty_files = []
    age_threshold_dt = current_time - datetime.timedelta(days=age_days)

    for root, dirs, files in os.walk(path):
        # Filter out excluded directories before processing files in them
        # Modify dirs in-place to prevent os.walk from descending into them
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), exclude_patterns)]

        for file in files:
            filepath = os.path.join(root, file)
            if is_excluded(filepath, exclude_patterns):
                continue

            try:
                # Get last modification time
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_dt = datetime.datetime.fromtimestamp(mtime_timestamp)

                if mtime_dt < age_threshold_dt:
                    dusty_files.append({
                        'path': filepath,
                        'last_modified': mtime_dt.isoformat()
                    })
            except OSError: # e.g., file not found, permissions error
                # print(f"Warning: Could not access file {filepath}")
                continue

    return dusty_files

def main():
    parser = argparse.ArgumentParser(
        description="Identify and report on old, potentially unused files (cosmic dust)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to scan for dusty files."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=90,
        help="Minimum age in days for a file to be considered 'dusty'. Defaults to 90."
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob-style pattern to exclude files/directories (can be repeated)."
    )
    parser.add_argument(
        "--output-format",
        type=str,
        choices=['text', 'json'],
        default='text',
        help="Output format: 'text' (default) or 'json'."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    current_time = datetime.datetime.now()
    dusty_files = collect_dust(args.path, args.age_days, args.exclude, current_time=current_time)

    if args.output_format == 'json':
        output_data = {
            "scan_path": args.path,
            "age_threshold_days": args.age_days,
            "scan_date": current_time.isoformat(),
            "dusty_files": dusty_files
        }
        print(json.dumps(output_data, indent=2))
    else:
        print(f"Cosmic Dust Report for: {args.path} (older than {args.age_days} days)")
        print("-" * (len(args.path) + 40))
        if dusty_files:
            print(f"Found {len(dusty_files)} dusty files:")
            for file_info in dusty_files:
                print(f"  - {file_info['path']} (Last modified: {file_info['last_modified'].split('T')[0]})")
        else:
            print("No cosmic dust found. Your repository is sparkling clean!")


if __name__ == "__main__":
    main()
