import os
import argparse
from typing import List, Tuple

def collect_dust(path: str, max_size_kb: int = 1, exclude_dirs: List[str] = None) -> List[Tuple[str, float]]:
    """
    Scans a directory for files smaller than max_size_kb (or empty) and returns a list of them.

    Args:
        path (str): The root directory to scan.
        max_size_kb (int): Maximum file size in KB to consider as 'dust'.
        exclude_dirs (List[str]): List of directory names to exclude from the scan.

    Returns:
        List[Tuple[str, float]]: A list of tuples, where each tuple contains
                                  (file_path, file_size_in_kb).
    """
    if exclude_dirs is None:
        exclude_dirs = []

    dust_files = []
    max_size_bytes = max_size_kb * 1024

    for root, dirs, files in os.walk(path):
        # Modify dirs in-place to prune directories from the walk
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size_bytes = os.path.getsize(file_path)
                if file_size_bytes <= max_size_bytes:
                    dust_files.append((file_path, file_size_bytes / 1024.0))
            except OSError: # Handle cases where file might be inaccessible or disappear
                continue
    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for small, forgotten files (cosmic dust) and report them."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to begin scanning."
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=1,
        help="Maximum file size in kilobytes to consider as 'dust'. Defaults to 1 KB."
    )
    parser.add_argument(
        "--exclude",
        nargs='*',
        default=[],
        help="Space-separated list of directory names to exclude from the scan (e.g., .git, node_modules)."
    )

    args = parser.parse_args()

    print(f"Cosmic Dust Report for {args.path} (max size: {args.max_size_kb} KB):\n" +
          "---------------------------------------------------")

    dust_files = collect_dust(args.path, args.max_size_kb, args.exclude)

    if dust_files:
        print(f"\nFound {len(dust_files)} pieces of cosmic dust:")
        for file_path, size_kb in dust_files:
            print(f"- {file_path} ({size_kb:.1f} KB)")
    else:
        print("\nNo cosmic dust found. Your repository is sparkling clean!")

    print("\n---------------------------------------------------")
    print(f"Scan complete. Total dust collected: {len(dust_files)} files.")

if __name__ == "__main__":
    main()
