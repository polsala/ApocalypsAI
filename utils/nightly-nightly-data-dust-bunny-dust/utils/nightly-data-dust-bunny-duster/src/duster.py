import os
import sys
from typing import List, Tuple

def find_empty_directories(root_dir: str) -> List[str]:
    """
    Finds all empty directories within the given root_dir.
    A directory is considered empty if it contains no files and no subdirectories.
    """
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def find_zero_byte_files(root_dir: str) -> List[str]:
    """
    Finds all zero-byte files within the given root_dir.
    """
    zero_byte_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                if os.path.isfile(filepath) and os.path.getsize(filepath) == 0:
                    zero_byte_files.append(filepath)
            except OSError:
                # Handle cases where file might be deleted or permissions issue
                pass
    return zero_byte_files

def duster_main(path_to_scan: str, delete_mode: bool = False) -> Tuple[List[str], List[str]]:
    """
    Main function to orchestrate the dusting process.
    Returns a tuple of (deleted_files, deleted_dirs).
    """
    if not os.path.isdir(path_to_scan):
        print(f"Error: Path '{path_to_scan}' is not a valid directory.", file=sys.stderr)
        return [], []

    print(f"Scanning '{path_to_scan}' for digital dust bunnies...")

    empty_dirs = find_empty_directories(path_to_scan)
    zero_byte_files = find_zero_byte_files(path_to_scan)

    deleted_files = []
    deleted_dirs = []

    if zero_byte_files:
        print("\n--- Zero-byte files found ---")
        for f in zero_byte_files:
            print(f"- File: {f}")
            if delete_mode:
                try:
                    os.remove(f)
                    deleted_files.append(f)
                    print(f"  [DELETED] {f}")
                except OSError as e:
                    print(f"  [ERROR] Could not delete {f}: {e}", file=sys.stderr)
        if not delete_mode:
            print("  (Run with --delete to remove these files)")
    else:
        print("\nNo zero-byte files found. Your digital pantry is clean!")

    if empty_dirs:
        # Sort empty_dirs in reverse order to delete deepest first
        empty_dirs.sort(key=lambda x: x.count(os.sep), reverse=True)
        print("\n--- Empty directories found ---")
        for d in empty_dirs:
            print(f"- Directory: {d}")
            if delete_mode:
                try:
                    os.rmdir(d)
                    deleted_dirs.append(d)
                    print(f"  [DELETED] {d}")
                except OSError as e:
                    print(f"  [ERROR] Could not delete {d}: {e}", file=sys.stderr)
        if not delete_mode:
            print("  (Run with --delete to remove these directories)")
    else:
        print("\nNo empty directories found. Your digital shelves are full of purpose!")

    if not zero_byte_files and not empty_dirs:
        print("\nAll clear! No digital dust bunnies detected in this sector.")
    elif delete_mode:
        print(f"\nCleanup complete. Removed {len(deleted_files)} files and {len(deleted_dirs)} directories.")
    else:
        print("\nReport complete. No changes made. Use --delete to perform cleanup.")

    return deleted_files, deleted_dirs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/duster.py <path_to_scan> [--delete]", file=sys.stderr)
        sys.exit(1)

    scan_path = sys.argv[1]
    should_delete = "--delete" in sys.argv

    duster_main(scan_path, should_delete)
    sys.exit(0)
