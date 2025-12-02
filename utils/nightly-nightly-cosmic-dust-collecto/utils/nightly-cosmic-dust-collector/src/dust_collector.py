import os
import shutil
import argparse
from typing import List, Tuple, Optional

def collect_dust(target_dir: str, max_size_bytes: int = 1024, quarantine_dir: Optional[str] = None) -> List[Tuple[str, int]]:
    """
    Scans a target directory for files smaller than or equal to max_size_bytes
    and optionally moves them to a quarantine directory.

    Args:
        target_dir (str): The root directory to scan.
        max_size_bytes (int): The maximum size (in bytes) for a file to be considered 'dust'.
        quarantine_dir (Optional[str]): If provided, files will be moved here. Otherwise, only reported.

    Returns:
        List[Tuple[str, int]]: A list of (filepath, size) tuples for identified dust files.
    """
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist or is not a directory.")
        return []

    if quarantine_dir:
        os.makedirs(quarantine_dir, exist_ok=True)

    dust_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                if os.path.isfile(filepath):
                    file_size = os.path.getsize(filepath)
                    if file_size <= max_size_bytes:
                        dust_files.append((filepath, file_size))
                        if quarantine_dir:
                            # Ensure unique name in quarantine to avoid overwrites
                            # Use relative path structure to preserve context
                            relative_path = os.path.relpath(filepath, target_dir)
                            quarantine_filepath = os.path.join(quarantine_dir, relative_path)
                            
                            # Create parent directories in quarantine_dir if they don't exist
                            os.makedirs(os.path.dirname(quarantine_filepath), exist_ok=True)
                            
                            print(f"Moving '{filepath}' ({file_size} bytes) to quarantine '{quarantine_filepath}'")
                            shutil.move(filepath, quarantine_filepath)
            except OSError as e:
                print(f"Warning: Could not process file '{filepath}': {e}")

    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans for small/empty files and optionally quarantines them."
    )
    parser.add_argument(
        "target_directory",
        type=str,
        help="The root directory to start scanning for cosmic dust."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024, # Default to 1KB
        help="The maximum file size (in bytes) to consider as 'cosmic dust'. Defaults to 1024 bytes."
    )
    parser.add_argument(
        "--quarantine-dir",
        type=str,
        default=None,
        help="If provided, identified files will be moved to this directory. Otherwise, files are only reported."
    )

    args = parser.parse_args()

    print(f"\n--- Nightly Cosmic Dust Collector ---\n")
    print(f"Scanning '{args.target_directory}' for files <= {args.max_size} bytes...")

    dust_files = collect_dust(args.target_directory, args.max_size, args.quarantine_dir)

    if dust_files:
        print(f"\n--- Identified Cosmic Dust ({len(dust_files)} files) ---")
        for filepath, size in dust_files:
            print(f"  - {filepath} ({size} bytes)")
        if args.quarantine_dir:
            print(f"\nAll identified dust files have been moved to '{args.quarantine_dir}'.")
        else:
            print(f"\nTo quarantine these files, re-run with '--quarantine-dir <path>'.")
    else:
        print("\nNo cosmic dust found. Your repository is sparkling clean!")

    print(f"\n-------------------------------------\n")

if __name__ == "__main__":
    main()
