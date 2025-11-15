import os
import time
import argparse
import fnmatch

def find_dust_bunnies(path, age_days, ignore_patterns=None):
    """
    Scans the given path for files and directories older than age_days.

    Args:
        path (str): The root directory to scan.
        age_days (int): The age threshold in days.
        ignore_patterns (list): A list of glob-style patterns to ignore.

    Returns:
        list: A list of paths to 'dust bunnies' (old files/directories).
    """
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return []

    threshold_timestamp = time.time() - (age_days * 24 * 60 * 60)
    dust_bunnies = []

    for root, dirs, files in os.walk(path, topdown=True):
        # Filter out ignored directories first to avoid walking them
        if ignore_patterns:
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)]

        for name in files:
            full_path = os.path.join(root, name)
            if ignore_patterns and any(fnmatch.fnmatch(name, p) for p in ignore_patterns):
                continue
            try:
                mtime = os.path.getmtime(full_path)
                if mtime < threshold_timestamp:
                    dust_bunnies.append(full_path)
            except OSError:
                # Handle cases where file might be deleted during scan or permissions issue
                pass

        for name in dirs:
            full_path = os.path.join(root, name)
            # Directories are checked after files in their root, as os.walk already filtered them
            try:
                mtime = os.path.getmtime(full_path)
                if mtime < threshold_timestamp:
                    dust_bunnies.append(full_path)
            except OSError:
                pass

    return dust_bunnies


def main():
    parser = argparse.ArgumentParser(
        description="Identify and list old, unused files and directories ('digital dust bunnies')."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=90,
        help="The age threshold in days. Defaults to 90."
    )
    parser.add_argument(
        "--ignore",
        action="append",
        default=[],
        help="Glob-style pattern to ignore files or directories. Can be specified multiple times."
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for items older than {args.age} days...")
    dust_bunnies = find_dust_bunnies(args.path, args.age, args.ignore)

    if dust_bunnies:
        print("\nFound the following digital dust bunnies:")
        for bunny in dust_bunnies:
            print(f"- {bunny}")
    else:
        print("\nNo digital dust bunnies found. Your workspace is sparkling clean!")


if __name__ == "__main__":
    main()
