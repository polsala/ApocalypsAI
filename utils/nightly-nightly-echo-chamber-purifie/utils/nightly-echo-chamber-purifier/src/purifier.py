import os
import hashlib
import argparse
import fnmatch

CHUNK_SIZE = 65536  # 64KB

def calculate_file_hash(filepath: str) -> str:
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Warning: Could not read file {filepath} - {e}")
        return ""

def find_duplicate_files(root_dir: str, exclude_patterns: list[str], min_size: int) -> dict[str, list[str]]:
    """Finds duplicate files in the given root directory.

    Args:
        root_dir: The directory to scan.
        exclude_patterns: A list of glob patterns to exclude files/directories.
        min_size: Minimum file size in bytes to consider.

    Returns:
        A dictionary where keys are file hashes and values are lists of file paths
        that share that hash, containing only groups with more than one file.
    ""
    hashes: dict[str, list[str]] = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out excluded directories in-place for os.walk efficiency
        dirnames[:] = [d for d in dirnames if not any(fnmatch.fnmatch(os.path.join(dirpath, d), p) for p in exclude_patterns)]

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.isfile(filepath):
                continue

            # Check for exclusion patterns for files
            if any(fnmatch.fnmatch(filepath, p) for p in exclude_patterns):
                continue

            try:
                file_size = os.path.getsize(filepath)
                if file_size < min_size:
                    continue
            except OSError as e:
                print(f"Warning: Could not get size for {filepath} - {e}")
                continue

            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes.setdefault(file_hash, []).append(filepath)

    # Filter out unique files (those with only one path per hash)
    duplicate_groups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Detect duplicate files in a directory based on content hash."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to start scanning for duplicates."
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="A glob pattern to exclude files or directories (e.g., *.log, temp/*). Can be specified multiple times."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=1, # Default to 1 byte to include almost all files
        help="Only consider files larger than this size (in bytes). Default is 1."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        exit(1)

    print(f"Scanning '{args.directory}' for duplicate files...")
    if args.exclude:
        print(f"Excluding patterns: {', '.join(args.exclude)}")
    if args.min_size > 1:
        print(f"Minimum file size: {args.min_size} bytes")

    duplicate_groups = find_duplicate_files(args.directory, args.exclude, args.min_size)

    if duplicate_groups:
        print("\n--- Duplicate Files Found ---")
        for file_hash, paths in duplicate_groups.items():
            print(f"\nHash: {file_hash}")
            for path in paths:
                print(f"  - {path}")
        print("\n--- End of Duplicates ---")
    else:
        print("\nNo duplicate files found.")

if __name__ == "__main__":
    main()
