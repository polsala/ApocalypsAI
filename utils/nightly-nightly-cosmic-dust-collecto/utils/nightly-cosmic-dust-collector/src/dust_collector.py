import os
import argparse
from typing import List, Tuple

def find_cosmic_dust(
    directory_path: str, threshold_bytes: int = 1024
) -> List[Tuple[str, int]]:
    """
    Scans a directory for files smaller than or equal to a specified threshold.

    Args:
        directory_path: The path to the directory to scan.
        threshold_bytes: The maximum file size in bytes to consider as "dust".

    Returns:
        A list of tuples, where each tuple contains the full path to a dust file
        and its size in bytes.
    """
    dust_files: List[Tuple[str, int]] = []
    ignored_dirs = ['.git', '.svn', '.hg', '__pycache__'] # Added __pycache__ for Python projects

    for root, dirs, files in os.walk(directory_path):
        # Modify dirs in-place to skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignored_dirs]

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Check if it's a regular file and get its size
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size <= threshold_bytes:
                        dust_files.append((file_path, file_size))
            except OSError:
                # Ignore files that cannot be accessed (e.g., broken symlinks, permission issues)
                pass
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for small, potentially forgotten files (cosmic dust)."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory to scan.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1024,  # Default to 1KB
        help="The maximum file size in bytes to consider as 'dust'. Defaults to 1024 bytes (1KB).",
    )

    args = parser.parse_args()

    print(
        f"Scanning {args.directory_path} for cosmic dust (threshold: {args.threshold} bytes)..."
    )

    dust_files = find_cosmic_dust(args.directory_path, args.threshold)

    if dust_files:
        print("\nCosmic Dust Found:")
        for file_path, file_size in dust_files:
            print(f"- {file_path} ({file_size} bytes)")
        print(f"\nTotal cosmic dust files found: {len(dust_files)}")
    else:
        print("\nNo cosmic dust found. Your directory is sparkling clean!")

if __name__ == "__main__":
    main()
