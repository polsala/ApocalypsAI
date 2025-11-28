import argparse
import hashlib
import os
import sys

CHUNK_SIZE = 65536  # 64KB

def calculate_file_hash(filepath: str) -> str | None:
    """Calculates the SHA256 hash of a file."""
    if not os.path.isfile(filepath):
        return None
    
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicates(directories: list[str], delete_duplicates: bool = False) -> dict[str, list[str]]:
    """
    Scans specified directories for duplicate files based on their SHA256 hash.
    Optionally deletes all but one instance of each duplicate group.
    
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    file_hashes: dict[str, list[str]] = {}
    all_files_scanned = 0
    
    print(f"Scanning {len(directories)} director{'y' if len(directories) == 1 else 'ies'} for duplicates...")

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not accessible: {directory}", file=sys.stderr)
            continue

        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                all_files_scanned += 1
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    file_hashes.setdefault(file_hash, []).append(filepath)
    
    duplicate_groups: dict[str, list[str]] = { 
        h: paths for h, paths in file_hashes.items() if len(paths) > 1
    }

    print(f"Scanned {all_files_scanned} files. Found {len(duplicate_groups)} groups of duplicates.")

    if delete_duplicates:
        print("\n--- Deleting Duplicates ---")
        deleted_count = 0
        for file_hash, paths in duplicate_groups.items():
            # Keep the first file, delete the rest
            files_to_delete = paths[1:]
            for filepath in files_to_delete:
                try:
                    os.remove(filepath)
                    print(f"  Deleted: {filepath}")
                    deleted_count += 1
                except OSError as e:
                    print(f"  Error deleting {filepath}: {e}", file=sys.stderr)
        print(f"Deleted {deleted_count} duplicate files.")
    else:
        if duplicate_groups:
            print("\n--- Duplicate Files Found (Report Only) ---")
            for file_hash, paths in duplicate_groups.items():
                print(f"Hash: {file_hash}")
                for filepath in paths:
                    print(f"  - {filepath}")
                print()
        else:
            print("No duplicate files found.")
            
    return duplicate_groups

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Scans directories for duplicate files."
    )
    parser.add_argument(
        "--path", 
        action="append", 
        required=True, 
        help="Path to a directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--delete-duplicates", 
        action="store_true", 
        help="Delete all but one instance of each duplicate file group."
    )

    args = parser.parse_args()

    if not args.path:
        print("Error: At least one --path must be provided.", file=sys.stderr)
        sys.exit(1)

    try:
        find_duplicates(args.path, args.delete_duplicates)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
