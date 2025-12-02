import os
import shutil
import argparse
import sys

DEFAULT_MAX_SIZE_KB = 1.0 # 1 KB

def _is_dust(filepath: str, max_size_bytes: int) -> bool:
    """Checks if a file is considered 'cosmic dust' based on its size."""
    try:
        file_size = os.path.getsize(filepath)
        return file_size <= max_size_bytes
    except OSError:
        # File might have been deleted or become inaccessible between walk and getsize
        return False

def _perform_action(filepath: str, action: str, archive_dir: str | None = None) -> None:
    """Performs the specified action (delete or archive) on a file."""
    if action == 'delete':
        print(f"  Deleting: {filepath}")
        os.remove(filepath)
    elif action == 'archive':
        if not archive_dir:
            print(f"  Skipping archive for {filepath}: --archive-dir not specified.")
            return
        os.makedirs(archive_dir, exist_ok=True)
        dest_path = os.path.join(archive_dir, os.path.basename(filepath))
        # Handle potential name collisions by appending a number
        counter = 1
        original_dest_path = dest_path
        while os.path.exists(dest_path):
            name, ext = os.path.splitext(original_dest_path)
            dest_path = f"{name}_{counter}{ext}"
            counter += 1

        print(f"  Archiving: {filepath} -> {dest_path}")
        shutil.move(filepath, dest_path)

def collect_dust(
    path: str,
    max_size_kb: float,
    action: str,
    dry_run: bool,
    archive_dir: str | None = None
) -> int:
    """Collects 'cosmic dust' files in the given path based on size criteria.

    Args:
        path: The root directory to start scanning from.
        max_size_kb: Maximum file size in kilobytes to be considered dust.
        action: 'list', 'delete', or 'archive'.
        dry_run: If True, no actual file system changes are made.
        archive_dir: Directory to move files to if action is 'archive'.

    Returns:
        The number of dust files found.
    """
    max_size_bytes = int(max_size_kb * 1024)
    dust_files_found = 0

    print(f"Scanning '{path}' for files <= {max_size_kb} KB...")

    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if _is_dust(filepath, max_size_bytes):
                dust_files_found += 1
                if action == 'list':
                    print(f"- Found dust: {filepath} ({os.path.getsize(filepath)} bytes)")
                else:
                    print(f"- Identified dust: {filepath} ({os.path.getsize(filepath)} bytes)")
                    if dry_run:
                        print(f"  (Dry run: would {action} {filepath})")
                    else:
                        _perform_action(filepath, action, archive_dir)
    
    print(f"\nScan complete. Found {dust_files_found} 'cosmic dust' files.")
    if dry_run and dust_files_found > 0 and action != 'list':
        print("No changes were made due to --dry-run. Remove --dry-run to apply changes.")
    
    return dust_files_found

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans for and manages small/empty files."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        default='.', 
        help="Root directory to scan for cosmic dust. Defaults to current directory."
    )
    parser.add_argument(
        '--max-size', 
        type=float, 
        default=DEFAULT_MAX_SIZE_KB, 
        help=f"Maximum file size in KB to be considered dust. Defaults to {DEFAULT_MAX_SIZE_KB} KB."
    )
    parser.add_argument(
        '--action', 
        type=str, 
        choices=['list', 'delete', 'archive'], 
        default='list', 
        help="Action to perform on identified dust files: 'list', 'delete', or 'archive'."
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help="If set, no actual file system changes will be made (implies 'list' action for output, but shows what *would* happen for 'delete'/'archive')."
    )
    parser.add_argument(
        '--archive-dir', 
        type=str, 
        help="Directory to move archived files to. Required if --action is 'archive' and not in dry-run mode."
    )

    args = parser.parse_args()

    if args.action == 'archive' and not args.archive_dir and not args.dry_run:
        print("Error: --archive-dir is required when --action is 'archive' and not in dry-run mode.", file=sys.stderr)
        sys.exit(1)

    collect_dust(
        path=args.path,
        max_size_kb=args.max_size,
        action=args.action,
        dry_run=args.dry_run,
        archive_dir=args.archive_dir
    )

if __name__ == '__main__':
    main()
