import os
import shutil
import argparse
import sys

def find_dust_files(path, max_size, empty_only):
    """Recursively finds files considered 'cosmic dust' in the given path."""
    dust_files = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                is_empty = file_size == 0

                if empty_only:
                    if is_empty:
                        dust_files.append((file_path, file_size))
                elif file_size <= max_size:
                    dust_files.append((file_path, file_size))
            except OSError as e:
                # Handle cases where file might be inaccessible or disappear during walk
                print(f"Warning: Could not access file {file_path}: {e}", file=sys.stderr)
                continue
    return dust_files

def list_dust_files(dust_files):
    """Prints the list of identified dust files."""
    if not dust_files:
        print("No cosmic dust found. Your repository is sparkling clean!")
        return

    print("\n--- Cosmic Dust Report ---")
    for file_path, file_size in dust_files:
        print(f"- {file_path} ({file_size} bytes)")
    print("--------------------------\n")

def archive_dust_files(dust_files, base_path, archive_dir_name, dry_run):
    """Moves dust files to an archive directory."""
    if not dust_files:
        print("No cosmic dust to archive.")
        return

    archive_path = os.path.join(base_path, archive_dir_name)

    if dry_run:
        print(f"Dry run: Would create archive directory: {archive_path}")
        print("Dry run: Would move the following files to archive:")
        for file_path, _ in dust_files:
            print(f"  - {file_path}")
        return

    print(f"Creating archive directory: {archive_path}")
    os.makedirs(archive_path, exist_ok=True)

    print("Archiving cosmic dust...")
    for file_path, _ in dust_files:
        try:
            # Construct a unique destination path to avoid name collisions
            # by preserving relative path structure within the archive
            relative_path = os.path.relpath(file_path, base_path)
            dest_path = os.path.join(archive_path, relative_path)
            dest_dir = os.path.dirname(dest_path)
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(file_path, dest_path)
            print(f"Archived: {file_path} -> {dest_path}")
        except Exception as e:
            print(f"Error archiving {file_path}: {e}", file=sys.stderr)

def delete_dust_files(dust_files, dry_run):
    """Deletes dust files."""
    if not dust_files:
        print("No cosmic dust to delete.")
        return

    if dry_run:
        print("Dry run: Would delete the following files:")
        for file_path, _ in dust_files:
            print(f"  - {file_path}")
        return

    print("Deleting cosmic dust...")
    for file_path, _ in dust_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Identify and manage small, forgotten files."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--mode",
        choices=['list', 'archive', 'delete'],
        default='list',
        help="Operation mode: 'list' (default), 'archive', or 'delete'."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024,
        help="Maximum file size in bytes to consider as dust. Default: 1024 bytes (1KB)."
    )
    parser.add_argument(
        "--empty-only",
        action='store_true',
        help="Only consider empty files as dust, ignoring --max-size."
    )
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help="Show what would be done without making any changes."
    )
    parser.add_argument(
        "--archive-dir",
        type=str,
        default=".dust_archive",
        help="Name of the subdirectory to move archived files into. Default: .dust_archive."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning '{args.path}' for cosmic dust (max size: {args.max_size} bytes, empty only: {args.empty_only})...")
    dust_files = find_dust_files(args.path, args.max_size, args.empty_only)

    if args.mode == 'list':
        list_dust_files(dust_files)
    elif args.mode == 'archive':
        archive_dust_files(dust_files, args.path, args.archive_dir, args.dry_run)
    elif args.mode == 'delete':
        delete_dust_files(dust_files, args.dry_run)

    if not dust_files and args.mode != 'list':
        sys.exit(2) # No-op, nothing to change
    elif dust_files and not args.dry_run and (args.mode == 'archive' or args.mode == 'delete'):
        sys.exit(0) # Success, changes made
    elif dust_files and args.dry_run:
        sys.exit(0) # Success, dry run showed changes
    else:
        sys.exit(0) # List mode or no dust found

if __name__ == "__main__":
    main()
