import os
import time
import argparse
from datetime import datetime, timedelta
import fnmatch

def find_dust_bunnies(
    target_path: str,
    min_age_days: int = 365,
    extra_patterns: list[str] = None
) -> dict:
    """
    Scans the target_path for 'digital dust bunnies':
    - Empty directories
    - Files older than min_age_days
    - Files matching common temporary/log patterns or extra_patterns

    Args:
        target_path: The root directory to scan.
        min_age_days: Files older than this many days will be flagged.
        extra_patterns: A list of additional glob patterns to match (e.g., ['*.bak']).

    Returns:
        A dictionary containing lists of identified dust bunnies.
    """
    dust_bunnies = {
        "empty_dirs": [],
        "ancient_files": [],
        "pattern_files": []
    }

    now = time.time()
    age_threshold_timestamp = now - (min_age_days * 24 * 60 * 60)

    # Common patterns for temporary/log files
    default_patterns = [
        "*.log", "*.tmp", "*.temp", "*.bak", "*.old",
        "__pycache__", ".DS_Store", "Thumbs.db",
        "*.swp", "*.swo", "*.swn",  # Vim swap files
        "*.pyc", "*.pyo", # Python compiled files
        "*.obj", "*.exe", "*.dll", "*.so", "*.dylib", # Compiled binaries (might be build artifacts)
        "npm-debug.log", "yarn-debug.log",
        "node_modules", # Often large and can be rebuilt
        ".pytest_cache", ".mypy_cache", ".ruff_cache", # Caches
        ".vscode", ".idea", # IDE specific folders
    ]
    all_patterns = default_patterns
    if extra_patterns:
        all_patterns.extend(extra_patterns)

    for root, dirs, files in os.walk(target_path):
        # Check for empty directories
        if not dirs and not files and os.path.isdir(root):
            dust_bunnies["empty_dirs"].append(root)

        for file_name in files:
            file_path = os.path.join(root, file_name)

            # Check for ancient files
            try:
                mtime = os.path.getmtime(file_path)
                if mtime < age_threshold_timestamp:
                    dust_bunnies["ancient_files"].append((file_path, datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')))
            except OSError:
                # File might have been deleted between os.walk and os.path.getmtime
                continue

            # Check for pattern-matched files
            for pattern in all_patterns:
                if fnmatch.fnmatch(file_name, pattern):
                    # Avoid adding the same file multiple times if it matches multiple patterns
                    if file_path not in [f[0] if isinstance(f, tuple) else f for f in dust_bunnies["pattern_files"]]:
                        dust_bunnies["pattern_files"].append(file_path)
                    break # Move to next file after first pattern match

        # Check for pattern-matched directories (like node_modules)
        for dir_name in list(dirs): # Iterate over a copy to allow modification
            dir_path = os.path.join(root, dir_name)
            for pattern in all_patterns:
                if fnmatch.fnmatch(dir_name, pattern):
                    if dir_path not in [f[0] if isinstance(f, tuple) else f for f in dust_bunnies["pattern_files"]]:
                        dust_bunnies["pattern_files"].append(dir_path)
                    dirs.remove(dir_name) # Don't recurse into matched directories
                    break

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Sweep your digital space for dust bunnies (old, temporary, or empty files/folders)."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root directory to scan for dust bunnies. Defaults to current directory."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=365,
        help="Files older than this many days will be flagged as 'ancient'. Defaults to 365."
    )
    parser.add_argument(
        "--patterns",
        type=str,
        help="Comma-separated list of additional glob patterns to flag (e.g., '*.bak,*.old')."
    )

    args = parser.parse_args()

    target_path = os.path.abspath(args.path)
    if not os.path.isdir(target_path):
        print(f"Error: The specified path '{target_path}' is not a valid directory.")
        exit(1)

    extra_patterns = args.patterns.split(',') if args.patterns else []

    print(f"Scanning {target_path} for digital dust bunnies...")
    dust_bunnies = find_dust_bunnies(target_path, args.age, extra_patterns)

    total_bunnies = (
        len(dust_bunnies["empty_dirs"]) +
        len(dust_bunnies["ancient_files"]) +
        len(dust_bunnies["pattern_files"])
    )

    print("\n--- Digital Dust Bunny Report ---\n")

    if dust_bunnies["empty_dirs"]:
        print("🧹 Empty Directories:")
        for d in dust_bunnies["empty_dirs"]:
            print(f"  - {d}")
        print()

    if dust_bunnies["ancient_files"]:
        print(f"⏳ Ancient Files (older than {args.age} days):")
        for f, mtime_str in dust_bunnies["ancient_files"]:
            print(f"  - {f} (Last modified: {mtime_str})")
        print()

    if dust_bunnies["pattern_files"]:
        print("🗑️ Temporary/Pattern-Matched Files & Directories:")
        for f in dust_bunnies["pattern_files"]:
            print(f"  - {f}")
        print()

    if total_bunnies == 0:
        print("🎉 No digital dust bunnies found! Your digital space is sparkling clean.")
    else:
        print(f"--- End Report ---")
        print(f"Found {total_bunnies} digital dust bunnies. Time for a cleanup!")

if __name__ == "__main__":
    main()
