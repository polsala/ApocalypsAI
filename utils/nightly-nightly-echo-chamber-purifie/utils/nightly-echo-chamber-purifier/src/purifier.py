import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath: str, block_size: int = 65536) -> str:
    """
    Calculates the SHA256 hash of a file.

    Args:
        filepath: The path to the file.
        block_size: The size of blocks to read from the file.

    Returns:
        The SHA256 hash as a hexadecimal string.
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return ""
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return ""

def find_duplicates(directory: str) -> dict[str, list[str]]:
    """
    Scans a directory for duplicate files based on their SHA256 hash.

    Args:
        directory: The path to the directory to scan.

    Returns:
        A dictionary where keys are SHA256 hashes and values are lists of file paths
        that share that hash, containing only groups with more than one file.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory not found or is not a directory: {directory}")
        return {}

    hash_map = defaultdict(list)
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = calculate_file_hash(filepath)
            if file_hash: # Only add if hash calculation was successful
                hash_map[file_hash].append(filepath)

    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Find duplicate files in a directory."
    )
    parser.add_argument(
        "--directory",
        type=str,
        required=True,
        help="The path to the directory to scan for duplicate files."
    )
    args = parser.parse_args()

    print(f"Scanning for duplicates in: {args.directory}")
    duplicate_groups = find_duplicates(args.directory)

    if duplicate_groups:
        print("---\nFound {} groups of duplicate files:\n".format(len(duplicate_groups)))
        for i, (file_hash, paths) in enumerate(duplicate_groups.items(), 1):
            print(f"Group {i} (Hash: {file_hash[:10]}...)") # Show first 10 chars of hash
            for path in paths:
                print(f"  - {path}")
            print() # Newline for readability
    else:
        print("---\nNo duplicate files found.")
    print("Scan complete.")

if __name__ == "__main__":
    main()
