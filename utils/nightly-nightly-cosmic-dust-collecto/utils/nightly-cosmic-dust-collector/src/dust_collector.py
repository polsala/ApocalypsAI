import os
import shutil
import time
import argparse
from datetime import datetime

def collect_dust(
    target_path: str,
    age_days: int = 30,
    dry_run: bool = False,
    dust_bin_name: str = ".cosmic-dust-bin",
) -> dict:
    """
    Identifies and optionally 'collects' (moves) stale files and removes empty directories.

    Args:
        target_path: The root directory to scan.
        age_days: Minimum age in days for a file to be considered stale.
        dry_run: If True, only report actions, don't modify filesystem.
        dust_bin_name: Name of the directory to move stale files into.

    Returns:
        A dictionary summarizing the actions taken or proposed.
    """
    if not os.path.exists(target_path):
        return {"status": "error", "message": f"Target path '{target_path}' does not exist."}
    if not os.path.isdir(target_path):
        return {"status": "error", "message": f"Target path '{target_path}' is not a directory."}

    stale_files = []
    empty_dirs = []
    current_time = time.time()
    age_seconds = age_days * 24 * 60 * 60

    # Store directories to check for emptiness after files are processed
    all_dirs = []

    print(f"\n--- Cosmic Dust Collection Report ({'Dry Run' if dry_run else 'Live Run'}) ---")
    print(f"Scanning: {target_path}")
    print(f"Stale file age threshold: {age_days} days")

    for root, dirs, files in os.walk(target_path, topdown=False): # topdown=False for removing empty dirs correctly
        all_dirs.append(root)

        for file in files:
            file_path = os.path.join(root, file)
            try:
                mod_time = os.path.getmtime(file_path)
                if (current_time - mod_time) > age_seconds:
                    stale_files.append(file_path)
            except OSError as e:
                print(f"Warning: Could not get modification time for {file_path}: {e}")

    # Check for empty directories, excluding the dust bin itself if it exists
    dust_bin_path = os.path.join(target_path, dust_bin_name)
    for d in all_dirs:
        if d == dust_bin_path: # Don't consider the dust bin itself for removal
            continue
        try:
            if not os.listdir(d):
                empty_dirs.append(d)
        except OSError as e:
            print(f"Warning: Could not list directory {d}: {e}")

    report = {
        "status": "success",
        "target_path": target_path,
        "age_days": age_days,
        "dry_run": dry_run,
        "dust_bin_name": dust_bin_name,
        "stale_files_found": len(stale_files),
        "empty_dirs_found": len(empty_dirs),
        "stale_files_list": stale_files,
        "empty_dirs_list": empty_dirs,
        "files_moved": [],
        "dirs_removed": [],
        "errors": []
    }

    if stale_files:
        print(f"\nIdentified {len(stale_files)} stale files:")
        for f in stale_files:
            print(f"  - {f}")
    else:
        print("\nNo stale files found.")

    if empty_dirs:
        print(f"\nIdentified {len(empty_dirs)} empty directories:")
        for d in empty_dirs:
            print(f"  - {d}")
    else:
        print("\nNo empty directories found.")

    if not dry_run:
        if stale_files:
            print(f"\n--- Moving stale files to '{dust_bin_name}' ---")
            os.makedirs(dust_bin_path, exist_ok=True)
            for file_path in stale_files:
                try:
                    dest_path = os.path.join(dust_bin_path, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                    report["files_moved"].append(file_path)
                    print(f"Moved: {file_path} -> {dest_path}")
                except Exception as e:
                    error_msg = f"Error moving {file_path}: {e}"
                    report["errors"].append(error_msg)
                    print(error_msg)

        if empty_dirs:
            print("\n--- Removing empty directories ---")
            # Sort in reverse order to ensure sub-directories are removed before parents
            for dir_path in sorted(empty_dirs, reverse=True):
                try:
                    # Re-check if directory is still empty, as moving files might have emptied a parent
                    if os.path.exists(dir_path) and os.path.isdir(dir_path) and not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        report["dirs_removed"].append(dir_path)
                        print(f"Removed: {dir_path}")
                    elif os.path.exists(dir_path) and os.path.isdir(dir_path) and os.listdir(dir_path):
                        print(f"Skipped removal of non-empty directory: {dir_path}")
                except OSError as e:
                    error_msg = f"Error removing {dir_path}: {e}"
                    report["errors"].append(error_msg)
                    print(error_msg)
    else:
        print("\n--- Dry Run Complete --- No changes were made. --- ")

    print("\n--- End of Report ---")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collects stale files and removes empty directories."
    )
    parser.add_argument("target_path", type=str, help="The root directory to scan.")
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered stale (default: 30).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="If set, only report actions, don't modify filesystem.",
    )
    parser.add_argument(
        "--dust-bin-name",
        type=str,
        default=".cosmic-dust-bin",
        help="Name of the directory to move stale files into (default: .cosmic-dust-bin).",
    )

    args = parser.parse_args()

    result = collect_dust(
        target_path=args.target_path,
        age_days=args.age,
        dry_run=args.dry_run,
        dust_bin_name=args.dust_bin_name,
    )

    if result.get("status") == "error":
        print(f"Error: {result['message']}")
        exit(1)
    elif result.get("stale_files_found") > 0 or result.get("empty_dirs_found") > 0:
        exit(0) # Indicate changes/findings
    else:
        exit(2) # Indicate no-op (nothing to change/find)
