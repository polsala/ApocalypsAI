import os
import argparse
from typing import List, Dict, Any

# Define common temporary file patterns
TEMP_FILE_PATTERNS = [
    ".tmp", ".log", ".bak", "~", ".swp", ".DS_Store", "Thumbs.db",
    "temp", "cache", ".cache", "__pycache__", ".pytest_cache",
    "npm-debug.log", "yarn-debug.log", "error.log"
]

def is_temp_file(filename: str) -> bool:
    """Checks if a filename matches any known temporary file patterns."""
    filename_lower = filename.lower()
    for pattern in TEMP_FILE_PATTERNS:
        if pattern.startswith('.'): # e.g., .tmp, .log, .DS_Store
            if filename_lower.endswith(pattern) or filename_lower == pattern:
                return True
        elif pattern.startswith('~'): # e.g., ~file.txt
            if filename_lower.startswith(pattern):
                return True
        elif pattern.startswith('__'): # e.g., __pycache__
            if pattern in filename_lower:
                return True
        elif pattern in filename_lower: # e.g., temp, cache, npm-debug.log
            return True
    return False

def find_dust_bunnies(root_paths: List[str]) -> Dict[str, List[str]]:
    """
    Scans specified root paths for digital dust bunnies (empty directories, temp files).
    Returns a dictionary with categories of dust bunnies found.
    """
    dust_bunnies: Dict[str, List[str]] = {
        "empty_directories": [],
        "temporary_files": []
    }

    for root_path in root_paths:
        if not os.path.exists(root_path):
            print(f"Warning: Path '{root_path}' does not exist. Skipping.")
            continue

        for dirpath, dirnames, filenames in os.walk(root_path):
            # Check for empty directories
            if not dirnames and not filenames:
                dust_bunnies["empty_directories"].append(dirpath)

            # Identify temporary files
            for filename in filenames:
                if is_temp_file(filename):
                    full_path = os.path.join(dirpath, filename)
                    dust_bunnies["temporary_files"].append(full_path)

    # Sort for deterministic output in tests
    dust_bunnies["empty_directories"].sort()
    dust_bunnies["temporary_files"].sort()

    return dust_bunnies

def report_dust_bunnies(dust_bunnies: Dict[str, List[str]]):
    """Prints a whimsical report of found dust bunnies."""
    total_bunnies = sum(len(lst) for lst in dust_bunnies.values())

    if total_bunnies == 0:
        print("\n✨ Your digital space is sparkling clean! No dust bunnies found. ✨")
        return

    print("\n--- Digital Dust Bunny Sweeper Report ---")
    print("Oh dear! It looks like we've found some digital dust bunnies lurking around.")

    if dust_bunnies["empty_directories"]:
        print("\n👻 Empty Directories (Ghostly Hollows):")
        for item in dust_bunnies["empty_directories"]:
            print(f"  - {item}")
        print(f"  ({len(dust_bunnies['empty_directories'])} empty directories found)")

    if dust_bunnies["temporary_files"]:
        print("\n🗑️ Temporary Files (Ephemeral Clutter):")
        for item in dust_bunnies["temporary_files"]:
            print(f"  - {item}")
        print(f"  ({len(dust_bunnies['temporary_files'])} temporary files found)")

    print(f"\nTotal Digital Dust Bunnies Spotted: {total_bunnies}")
    print("\nRecommendation: Consider tidying up these paths. Remember, I only suggest, I never delete!")
    print("----------------------------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Sweeper: Finds empty directories and temporary files."
    )
    parser.add_argument(
        "--path",
        nargs='+',
        required=True,
        help="One or more root paths to scan for dust bunnies."
    )
    args = parser.parse_args()

    print(f"Scanning {len(args.path)} path(s) for digital dust bunnies...")
    dust_bunnies = find_dust_bunnies(args.path)
    report_dust_bunnies(dust_bunnies)

if __name__ == "__main__":
    main()
