import os
import sys
import argparse
from datetime import datetime, timedelta
from fnmatch import fnmatch

def get_default_ignore_patterns():
    """Returns a list of common patterns to ignore."""
    return [
        '*.pyc',
        '__pycache__',
        '.git',
        '.DS_Store',
        '*.tmp',
        '*.bak',
        '.venv',
        'env',
        'node_modules',
        'dist',
        'build',
        'target',
        'out',
        'logs',
        '*.log',
        'npm-debug.log',
        'yarn-debug.log',
        'yarn-error.log',
        '.idea',
        '.vscode',
        '.pytest_cache',
        '.mypy_cache',
        '.ruff_cache',
        'coverage',
        '.coverage',
        'venv',
        '__pycache__',
        '*.swp',
        '*.swo'
    ]

def is_ignored(path, ignore_patterns):
    """Checks if a path matches any of the ignore patterns."""
    basename = os.path.basename(path)
    for pattern in ignore_patterns:
        if fnmatch(path, pattern) or fnmatch(basename, pattern):
            return True
    return False

def find_dust_bunnies(root_dir, age_days, ignore_patterns):
    """Finds files and directories older than age_days, excluding ignored patterns."""
    dust_bunnies = []
    cutoff_time = datetime.now() - timedelta(days=age_days)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Filter out ignored directories from dirnames *before* recursing
        # This prevents walking into ignored directories entirely
        dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(dirpath, d), ignore_patterns)]

        # Check current directory itself if it's old and not ignored
        if dirpath != root_dir and not is_ignored(dirpath, ignore_patterns):
            try:
                mod_timestamp = os.path.getmtime(dirpath)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)
                if mod_datetime < cutoff_time:
                    dust_bunnies.append(dirpath)
            except OSError:
                pass # Ignore if directory disappears or permissions issue

        for name in filenames:
            full_path = os.path.join(dirpath, name)
            if is_ignored(full_path, ignore_patterns):
                continue

            try:
                mod_timestamp = os.path.getmtime(full_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                if mod_datetime < cutoff_time:
                    dust_bunnies.append(full_path)
            except OSError: # Handle cases where file might be deleted during walk or permissions issue
                continue

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Identify and list old, unused files and directories (digital dust bunnies)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to scan for dust bunnies."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Files/directories older than this many days will be flagged. Default: 30."
    )
    parser.add_argument(
        "--ignore-patterns",
        type=str,
        default=",".join(get_default_ignore_patterns()),
        help="Comma-separated glob patterns to ignore. Default: common build/temp files."
    )

    args = parser.parse_args()

    root_path = os.path.abspath(args.path)
    if not os.path.isdir(root_path):
        print(f"Error: The provided path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    ignore_list = [p.strip() for p in args.ignore_patterns.split(',') if p.strip()]

    print(f"Scanning '{root_path}' for digital dust bunnies older than {args.age} days...")
    print(f"Ignoring patterns: {', '.join(ignore_list)}\n")

    dust_bunnies = find_dust_bunnies(root_path, args.age, ignore_list)

    if dust_bunnies:
        print("Found the following digital dust bunnies (suggested for deletion):\n")
        for bunny in sorted(dust_bunnies):
            print(bunny)
        print(f"\nTotal: {len(dust_bunnies)} items.")
        print("\nNote: This utility only lists items. It does NOT delete them.")
    else:
        print("No digital dust bunnies found! Your project is sparkling clean.")

if __name__ == "__main__":
    main()
