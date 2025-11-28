import os
import argparse
from pathlib import Path
from typing import List, Tuple

def find_dust_files(
    directory: Path,
    max_size_bytes: int,
    extensions: Tuple[str, ...]
) -> List[Path]:
    """
    Scans the given directory for 'cosmic dust' files:
    - Files smaller than or equal to max_size_bytes.
    - Files with extensions matching the provided list (case-insensitive).
    - Empty files are always considered dust, regardless of extension.
    """
    dust_files: List[Path] = []
    if not directory.is_dir():
        print(f"Warning: Directory '{directory}' does not exist or is not a directory.")
        return []

    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = Path(root) / file_name
            try:
                file_size = os.path.getsize(file_path)
                file_extension = file_path.suffix.lower()

                is_empty = file_size == 0
                is_small = file_size <= max_size_bytes
                is_matching_extension = file_extension in extensions

                if is_empty or (is_small and is_matching_extension):
                    dust_files.append(file_path)
            except FileNotFoundError:
                # File might have been deleted between os.walk and os.path.getsize
                continue
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                continue
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Cosmic Dust Collector: Scans directories for small, forgotten files."
    )
    parser.add_argument(
        "path",
        type=Path,
        help="The directory path to scan for cosmic dust."
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024,  # 1 KB
        help="Maximum file size in bytes to consider as 'dust'. Default is 1024 bytes (1KB)."
    )
    parser.add_argument(
        "--extensions",
        type=str,
        default=".tmp,.bak,.log,.old,.swp",
        help="Comma-separated list of file extensions (e.g., .tmp,.log) to consider as 'dust'. Empty files are always included. Default is '.tmp,.bak,.log,.old,.swp'."
    )

    args = parser.parse_args()

    target_directory = args.path
    max_size = args.max_size
    extensions_tuple = tuple(ext.strip().lower() for ext in args.extensions.split(',') if ext.strip())

    print(f"Scanning '{target_directory}' for cosmic dust...")
    print(f"  Max size for dust: {max_size} bytes")
    print(f"  Extensions for dust: {', '.join(extensions_tuple) if extensions_tuple else 'None (only empty files)'}")

    dust_files = find_dust_files(target_directory, max_size, extensions_tuple)

    if dust_files:
        print("\n--- Cosmic Dust Detected! ---")
        for dust_file in dust_files:
            try:
                size = os.path.getsize(dust_file)
                print(f"- {dust_file} ({size} bytes)")
            except FileNotFoundError:
                print(f"- {dust_file} (deleted before size check)")
        print(f"\nTotal {len(dust_files)} particles of cosmic dust found.")
        print("Consider reviewing these files for potential cleanup.")
    else:
        print("\nNo cosmic dust detected. Your digital cosmos is sparkling clean!")

if __name__ == "__main__":
    main()
