import argparse
import hashlib
import os
import sys

BLOCK_SIZE = 65536  # 64KB

def calculate_hash(filepath: str) -> str:
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(BLOCK_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return ""

def find_duplicates(paths: list[str]) -> dict[str, list[str]]:
    """Scans given paths for duplicate files based on content hash."""
    files_by_size = {}  # size -> [filepath1, filepath2, ...]
    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: Path not found: {path}", file=sys.stderr)
            continue
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if not os.path.islink(filepath) and os.path.isfile(filepath):
                    try:
                        size = os.path.getsize(filepath)
                        files_by_size.setdefault(size, []).append(filepath)
                    except OSError as e:
                        print(f"Error getting size of {filepath}: {e}", file=sys.stderr)

    duplicate_map = {}  # hash -> [filepath1, filepath2, ...]
    for size, filepaths in files_by_size.items():
        if size == 0: # Skip empty files, they are technically duplicates but often not what we want to manage
            continue
        if len(filepaths) > 1: # Only check files that have potential duplicates by size
            for filepath in filepaths:
                file_hash = calculate_hash(filepath)
                if file_hash:
                    duplicate_map.setdefault(file_hash, []).append(filepath)

    # Filter out entries that are not actually duplicates (i.e., only one file per hash)
    return {h: fpaths for h, fpaths in duplicate_map.items() if len(fpaths) > 1}

def process_duplicates(duplicate_map: dict[str, list[str]], action: str):
    """Performs the specified action on identified duplicate files."""
    if not duplicate_map:
        print("No duplicate files found.")
        return

    print(f"Processing {len(duplicate_map)} sets of duplicate files with action: {action}")

    for file_hash, filepaths in duplicate_map.items():
        # Sort paths for deterministic behavior (e.g., which one is 'kept')
        filepaths.sort()
        canonical_file = filepaths[0]
        duplicates_to_process = filepaths[1:]

        print(f"\n--- Duplicate Set (Hash: {file_hash[:10]}...) ---")
        print(f"  Canonical: {canonical_file}")

        if action == 'report':
            for dup_file in duplicates_to_process:
                print(f"  Duplicate: {dup_file}")

        elif action == 'delete':
            for dup_file in duplicates_to_process:
                try:
                    os.remove(dup_file)
                    print(f"  Deleted: {dup_file}")
                except OSError as e:
                    print(f"  Error deleting {dup_file}: {e}", file=sys.stderr)

        elif action == 'hardlink':
            for dup_file in duplicates_to_process:
                try:
                    # Check if the duplicate file exists and is not already a hardlink to the canonical
                    if os.path.exists(dup_file):
                        if os.stat(dup_file).st_ino == os.stat(canonical_file).st_ino:
                            print(f"  Already hardlinked: {dup_file}")
                            continue
                        os.remove(dup_file) # Remove the duplicate before creating hardlink
                    os.link(canonical_file, dup_file)
                    print(f"  Hardlinked: {dup_file} -> {canonical_file}")
                except OSError as e:
                    print(f"  Error hardlinking {dup_file} to {canonical_file}: {e}", file=sys.stderr)
        else:
            print(f"Unknown action: {action}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Find and manage duplicate files using content hashing."
    )
    parser.add_argument(
        "--paths",
        nargs='+',
        required=True,
        help="One or more paths to directories to scan for duplicates."
    )
    parser.add_argument(
        "--action",
        choices=['report', 'delete', 'hardlink'],
        required=True,
        help="Action to perform on identified duplicates: 'report', 'delete', or 'hardlink'."
    )

    args = parser.parse_args()

    duplicate_map = find_duplicates(args.paths)
    process_duplicates(duplicate_map, args.action)

if __name__ == "__main__":
    main()
