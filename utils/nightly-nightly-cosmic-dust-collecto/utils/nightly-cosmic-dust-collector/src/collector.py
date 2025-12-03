import os
import sys

def collect_dust(target_path, min_file_size_bytes=1, dry_run=True):
    """
    Scans a directory for empty folders and files smaller than a specified size.
    Optionally removes them.

    Args:
        target_path (str): The path to the directory to scan.
        min_file_size_bytes (int): Files smaller than this size (in bytes) will be considered "dust".
                                   Defaults to 1 (i.e., empty files).
        dry_run (bool): If True, only reports what would be removed. If False, performs removal.

    Returns:
        dict: A report containing lists of removed files and directories, and counts.
    """
    if not os.path.isdir(target_path):
        return {"error": f"Target path '{target_path}' is not a valid directory."}

    removed_files = []
    removed_dirs = []
    total_space_freed = 0

    # First pass: identify and remove small files
    for root, _, files in os.walk(target_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                file_size = os.path.getsize(file_path)
                if file_size < min_file_size_bytes:
                    if not dry_run:
                        os.remove(file_path)
                        removed_files.append(file_path)
                        total_space_freed += file_size
                    else:
                        removed_files.append(f"[DRY RUN] {file_path} ({file_size} bytes)")
            except OSError:
                # File might have been removed by another process, or permissions issue
                pass

    # Second pass: identify and remove empty directories
    # We walk topdown=False to ensure child directories are processed before parents
    for root, dirs, files in os.walk(target_path, topdown=False):
        # After removing small files, some directories might become empty
        # Re-check contents of the directory
        current_dir_contents = os.listdir(root)
        if not current_dir_contents: # If the directory is truly empty
            if root != target_path: # Don't remove the root target path itself
                if not dry_run:
                    try:
                        os.rmdir(root)
                        removed_dirs.append(root)
                    except OSError:
                        # Directory might not be empty anymore or permissions issue
                        pass
                else:
                    removed_dirs.append(f"[DRY RUN] {root}")

    return {
        "removed_files": removed_files,
        "removed_dirs": removed_dirs,
        "total_files_removed": len(removed_files),
        "total_dirs_removed": len(removed_dirs),
        "total_space_freed_bytes": total_space_freed if not dry_run else 0,
        "dry_run": dry_run
    }

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Cosmic Dust Collector: Scans for and optionally removes empty folders and tiny files."
    )
    parser.add_argument("path", help="The target directory to clean.")
    parser.add_argument(
        "--min-file-size",
        type=int,
        default=1,
        help="Files smaller than this size (in bytes) will be considered 'dust'. Default is 1 byte (empty files).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run: report what would be removed without actually deleting anything.",
    )

    args = parser.parse_args()

    print(f"Scanning '{args.path}' for cosmic dust...")
    report = collect_dust(args.path, args.min_file_size, args.dry_run)

    if "error" in report:
        print(f"Error: {report['error']}")
        sys.exit(1)

    print("\n--- Cosmic Dust Collection Report ---")
    print(f"Mode: {'Dry Run' if report['dry_run'] else 'Actual Removal'}")
    print(f"Files identified/removed: {report['total_files_removed']}")
    for f in report['removed_files']:
        print(f"  - {f}")
    print(f"Directories identified/removed: {report['total_dirs_removed']}")
    for d in report['removed_dirs']:
        print(f"  - {d}")

    if not report['dry_run']:
        print(f"Total space freed: {report['total_space_freed_bytes']} bytes")
    else:
        print("No files or directories were actually removed in dry run mode.")

    if report['total_files_removed'] == 0 and report['total_dirs_removed'] == 0:
        print("No cosmic dust found. Your digital space is pristine!")
    else:
        print("Cosmic dust collected. Your digital space is a bit cleaner now!")

if __name__ == "__main__":
    main()
