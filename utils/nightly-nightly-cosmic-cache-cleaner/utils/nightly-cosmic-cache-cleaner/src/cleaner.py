import os
import shutil
import argparse
from typing import List, Dict, Tuple

# Default configuration for files and directories to clean
# These are common temporary files, cache directories, and build artifacts.
DEFAULT_CLEAN_CONFIG = {
    "directories": [
        "__pycache__",
        ".pytest_cache",
        "build",
        "dist",
        ".mypy_cache",
        ".venv", # Often contains many files, be careful with this one.
        "env",   # Another common virtual environment name.
    ],
    "file_patterns": [
        "*.pyc",
        "*.log",
        ".DS_Store",  # macOS specific
        "Thumbs.db",  # Windows specific
        "*.bak",
        "*.tmp",
    ],
}

def get_cosmic_message(action: str, item: str) -> str:
    """Generates a whimsical cosmic message."""
    messages = {
        "scanning": f"🌌 Scanning the digital nebula for cosmic clutter in '{item}'...",
        "found_dir": f"✨ Discovered a temporal anomaly directory: '{item}'",
        "found_file": f"✨ Spotted a stray cosmic dust particle: '{item}'",
        "removing_dir": f"💫 Erasing temporal anomaly directory: '{item}'",
        "removing_file": f"💫 Vaporizing cosmic dust particle: '{item}'",
        "dry_run_dir": f"🔭 (Dry Run) Would erase temporal anomaly directory: '{item}'",
        "dry_run_file": f"🔭 (Dry Run) Would vaporize cosmic dust particle: '{item}'",
        "summary_start": "🌠 Cosmic Cleansing Complete! Here's the celestial report:",
        "summary_dirs": f"  - {item} temporal anomaly directories erased.",
        "summary_files": f"  - {item} cosmic dust particles vaporized.",
        "no_clutter": "🧘 Your digital nebula is pristine. No cosmic clutter found!",
        "start": "🚀 Initiating Nightly Cosmic Cache Cleanser...",
        "end": "✅ Cosmic cleansing operations concluded. May your code be ever clean!",
    }
    return messages.get(action, f"🌌 Performing unknown cosmic action on: '{item}'")

def clean_project(
    path: str,
    config: Dict[str, List[str]],
    dry_run: bool = True,
    verbose: bool = False,
) -> Tuple[int, int]:
    """
    Cleans a project directory by removing specified files and directories.

    Args:
        path (str): The root path of the project to clean.
        config (Dict[str, List[str]]): A dictionary containing 'directories' and 'file_patterns' to target.
        dry_run (bool): If True, only report what would be removed without actual deletion.
        verbose (bool): If True, print detailed messages for each item found/removed.

    Returns:
        Tuple[int, int]: A tuple containing (directories_removed_count, files_removed_count).
    """
    if not os.path.isdir(path):
        print(f"❌ Error: Path '{path}' is not a valid directory. Aborting cosmic mission.")
        return 0, 0

    print(get_cosmic_message("start", ""))
    print(get_cosmic_message("scanning", os.path.abspath(path)))

    directories_to_remove: List[str] = []
    files_to_remove: List[str] = []

    for root, dirs, files in os.walk(path, topdown=True):
        # Handle directories
        for dname in list(dirs): # Iterate over a copy to allow modification of 'dirs'
            if dname in config["directories"]:
                full_path = os.path.join(root, dname)
                directories_to_remove.append(full_path)
                if verbose:
                    print(get_cosmic_message("found_dir", full_path))
                dirs.remove(dname) # Don't traverse into directories we plan to remove

        # Handle files
        for fname in files:
            for pattern in config["file_patterns"]:
                if fname.endswith(pattern[1:]) and pattern.startswith('*'): # Simple glob matching for now
                    full_path = os.path.join(root, fname)
                    files_to_remove.append(full_path)
                    if verbose:
                        print(get_cosmic_message("found_file", full_path))
                    break # Only add once per file

    dirs_removed_count = 0
    files_removed_count = 0

    # Perform removal
    for d_path in directories_to_remove:
        if dry_run:
            print(get_cosmic_message("dry_run_dir", d_path))
        else:
            try:
                shutil.rmtree(d_path)
                print(get_cosmic_message("removing_dir", d_path))
                dirs_removed_count += 1
            except OSError as e:
                print(f"⚠️ Failed to erase directory '{d_path}': {e}")

    for f_path in files_to_remove:
        if dry_run:
            print(get_cosmic_message("dry_run_file", f_path))
        else:
            try:
                os.remove(f_path)
                print(get_cosmic_message("removing_file", f_path))
                files_removed_count += 1
            except OSError as e:
                print(f"⚠️ Failed to vaporize file '{f_path}': {e}")

    print(get_cosmic_message("summary_start", ""))
    if dirs_removed_count == 0 and files_removed_count == 0:
        print(get_cosmic_message("no_clutter", ""))
    else:
        print(get_cosmic_message("summary_dirs", str(dirs_removed_count)))
        print(get_cosmic_message("summary_files", str(files_removed_count)))

    print(get_cosmic_message("end", ""))
    return dirs_removed_count, files_removed_count

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Cache Cleaner: Purify your digital nebula of cosmic clutter."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The root path of the project to clean. Defaults to current directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only report what would be removed without actual deletion.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="If set, print detailed messages for each item found/removed.",
    )
    args = parser.parse_args()

    clean_project(args.path, DEFAULT_CLEAN_CONFIG, args.dry_run, args.verbose)

if __name__ == "__main__":
    main()
