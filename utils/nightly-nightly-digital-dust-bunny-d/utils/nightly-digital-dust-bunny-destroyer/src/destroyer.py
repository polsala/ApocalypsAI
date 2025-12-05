import os
import shutil
import argparse
from datetime import datetime, timedelta

def _is_empty_dir(path):
    """Helper to check if a directory is truly empty (no files or subdirectories)."""
    return not any(os.scandir(path))

def clean_empty_directories(root_dir, dry_run=False):
    """Recursively finds and removes empty directories within root_dir."""
    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        return 0

    print(f"\n--- Cleaning Empty Directories in '{root_dir}' ---")
    removed_count = 0
    # Walk from bottom up to ensure subdirectories are removed first
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        if dirpath == root_dir: # Don't remove the root directory itself
            continue
        try:
            if _is_empty_dir(dirpath):
                if dry_run:
                    print(f"[DRY RUN] Would remove empty directory: {dirpath}")
                else:
                    os.rmdir(dirpath)
                    print(f"Removed empty directory: {dirpath}")
                    removed_count += 1
        except OSError as e:
            print(f"Error removing directory {dirpath}: {e}")
    print(f"Finished cleaning empty directories. Removed {removed_count} directories.")
    return removed_count

def clean_old_temp_files(root_dir, age_days=7, temp_patterns=None, dry_run=False):
    """Removes files matching temp_patterns older than age_days within root_dir."""
    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        return 0

    if temp_patterns is None:
        temp_patterns = ['.tmp', '.temp', '~', '.bak', '.log']

    print(f"\n--- Cleaning Old Temporary Files in '{root_dir}' (older than {age_days} days) ---")
    removed_count = 0
    cutoff_time = datetime.now() - timedelta(days=age_days)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not os.path.isfile(file_path): # Skip if it's not a file (e.g., broken symlink already handled)
                continue

            # Check for common temp file patterns
            is_temp = any(pattern in filename.lower() for pattern in temp_patterns)
            if not is_temp and filename.startswith('.'): # Also consider dotfiles as potential temp/config
                is_temp = True

            if is_temp:
                try:
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if mod_time < cutoff_time:
                        if dry_run:
                            print(f"[DRY RUN] Would remove old temp file: {file_path} (last modified: {mod_time.strftime('%Y-%m-%d')})")
                        else:
                            os.remove(file_path)
                            print(f"Removed old temp file: {file_path} (last modified: {mod_time.strftime('%Y-%m-%d')})")
                            removed_count += 1
                except OSError as e:
                    print(f"Error accessing or removing file {file_path}: {e}")
    print(f"Finished cleaning old temporary files. Removed {removed_count} files.")
    return removed_count

def clean_broken_symlinks(root_dir, dry_run=False):
    """Finds and removes broken symbolic links within root_dir."""
    if not os.path.isdir(root_dir):
        print(f"Error: '{root_dir}' is not a valid directory.")
        return 0

    print(f"\n--- Cleaning Broken Symbolic Links in '{root_dir}' ---")
    removed_count = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for entry in dirnames + filenames:
            full_path = os.path.join(dirpath, entry)
            if os.path.islink(full_path):
                # os.path.exists returns False for broken symlinks
                if not os.path.exists(full_path):
                    if dry_run:
                        print(f"[DRY RUN] Would remove broken symlink: {full_path}")
                    else:
                        os.remove(full_path)
                        print(f"Removed broken symlink: {full_path}")
                        removed_count += 1
    print(f"Finished cleaning broken symlinks. Removed {removed_count} links.")
    return removed_count

def main():
    parser = argparse.ArgumentParser(
        description="Digital Dust Bunny Destroyer: Cleans up empty directories, old temp files, and broken symlinks."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to scan and clean.'
    )
    parser.add_argument(
        '--age', 
        type=int, 
        default=7, 
        help='Number of days after which temporary files are considered old. Default is 7.'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='If present, only report what would be done, without making changes.'
    )

    args = parser.parse_args()

    print(f"\n--- Starting Digital Dust Bunny Destroyer for '{args.path}' (Dry Run: {args.dry_run}) ---")

    clean_empty_directories(args.path, args.dry_run)
    clean_old_temp_files(args.path, args.age, dry_run=args.dry_run)
    clean_broken_symlinks(args.path, args.dry_run)

    print(f"\n--- Digital Dust Bunny Destroyer finished. ---")

if __name__ == '__main__':
    main()
