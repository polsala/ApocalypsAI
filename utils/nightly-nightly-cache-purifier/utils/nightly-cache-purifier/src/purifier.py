import os
import shutil
import sys
import argparse
from typing import List, Tuple, Dict

def get_cache_paths() -> List[str]:
    """
    Determines common user-level cache directories based on the operating system.
    """
    paths = []
    home = os.path.expanduser("~")

    if sys.platform.startswith('linux') or sys.platform == 'darwin': # Linux and macOS
        paths.append(os.path.join(home, '.cache'))
        if sys.platform == 'darwin': # macOS specific
            paths.append(os.path.join(home, 'Library', 'Caches'))
        # Common tool caches
        paths.append(os.path.join(home, '.npm', '_cacache'))
        paths.append(os.path.join(home, '.cache', 'pip'))
    elif sys.platform == 'win32': # Windows
        temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
        if temp_dir:
            paths.append(temp_dir)
        local_app_data = os.environ.get('LOCALAPPDATA')
        if local_app_data:
            paths.append(os.path.join(local_app_data, 'Temp'))
            paths.append(os.path.join(local_app_data, 'pip', 'cache'))
        app_data = os.environ.get('APPDATA')
        if app_data:
            paths.append(os.path.join(app_data, 'npm-cache'))
    
    # Filter out paths that don't exist or are not directories
    return [p for p in paths if os.path.isdir(p)]

def get_dir_size(path: str) -> int:
    """
    Calculates the total size of a directory in bytes.
    """
    total_size = 0
    if not os.path.isdir(path):
        return total_size
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Skip if it's not a symbolic link and doesn't exist, or if it's a broken symlink
            if not os.path.islink(fp) and not os.path.exists(fp):
                continue
            try:
                total_size += os.path.getsize(fp)
            except OSError:
                # Handle cases where file might be inaccessible or disappear during walk
                pass
    return total_size

def format_bytes(bytes_val: int) -> str:
    """
    Formats a byte value into a human-readable string (e.g., 1.2 GB).
    """
    if bytes_val == 0:
        return "0 Bytes"
    sizes = ["Bytes", "KB", "MB", "GB", "TB"]
    i = 0
    while bytes_val >= 1024 and i < len(sizes) - 1:
        bytes_val /= 1024.0
        i += 1
    return f"{bytes_val:.2f} {sizes[i]}"

def dry_run_purifier(verbose: bool = False) -> Tuple[Dict[str, int], int]:
    """
    Performs a dry run, reporting on potential space savings.
    Returns a dictionary of paths and their sizes, and the total size.
    """
    print("✨ Initiating Nightly Cache Purifier Dry Run...")
    cache_paths = get_cache_paths()
    if not cache_paths:
        print("No common cache directories found to analyze.")
        return {}, 0

    total_potential_savings = 0
    path_sizes = {}

    print("\nDetected potential cache directories:")
    for path in cache_paths:
        size = get_dir_size(path)
        if size > 0:
            path_sizes[path] = size
            total_potential_savings += size
            print(f"  - {path}: {format_bytes(size)}")
            if verbose:
                for root, dirs, files in os.walk(path):
                    for name in dirs + files:
                        full_path = os.path.join(root, name)
                        try:
                            item_size = os.path.getsize(full_path) if os.path.isfile(full_path) else get_dir_size(full_path)
                            print(f"    - {full_path} ({format_bytes(item_size)})")
                        except OSError:
                            pass # Ignore inaccessible files/dirs

    print(f"\nTotal potential space to reclaim: {format_bytes(total_potential_savings)}")
    print("Dry run complete. No files were deleted.")
    return path_sizes, total_potential_savings

def clean_purifier(force: bool = False, verbose: bool = False) -> int:
    """
    Cleans detected cache directories.
    Returns the total space reclaimed.
    """
    print("🧹 Initiating Nightly Cache Purifier Cleanse...")
    path_sizes, total_potential_savings = dry_run_purifier(verbose=verbose)

    if not path_sizes:
        print("No cache directories with content found to clean.")
        return 0

    if not force:
        confirmation = input(f"\nProceed with cleaning {format_bytes(total_potential_savings)} from {len(path_sizes)} directories? (y/N): ").lower()
        if confirmation != 'y':
            print("Cleaning aborted by user.")
            return 0

    total_reclaimed_space = 0
    print("\nProceeding with cleaning...")
    for path, size in path_sizes.items():
        try:
            print(f"  - Deleting {path} ({format_bytes(size)})...")
            shutil.rmtree(path)
            total_reclaimed_space += size
            print(f"    Successfully deleted {path}.")
        except OSError as e:
            print(f"    Error deleting {path}: {e}")
    
    print(f"\nNightly Cache Purifier complete! Reclaimed: {format_bytes(total_reclaimed_space)}")
    return total_reclaimed_space

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cache Purifier: Cleans common user-level cache directories."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report potential space savings without deleting anything (default)."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Scan and prompt to delete detected caches."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Use with --clean to skip confirmation prompts and delete immediately. USE WITH EXTREME CAUTION!"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show more detailed output during scanning."
    )

    args = parser.parse_args()

    if args.clean:
        clean_purifier(force=args.force, verbose=args.verbose)
    else:
        dry_run_purifier(verbose=args.verbose)

if __name__ == "__main__":
    main()
