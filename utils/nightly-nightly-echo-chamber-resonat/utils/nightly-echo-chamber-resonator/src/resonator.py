import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm='sha256', buffer_size=65536):
    """
    Calculates the SHA256 hash of a file.
    """
    hasher = hashlib.new(hash_algorithm)
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(buffer_size)
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except IOError:
        return None # File not found or inaccessible

def find_duplicate_files(directory):
    """
    Scans the given directory and its subdirectories for duplicate files
    based on their SHA256 hash.
    Returns a dictionary where keys are file hashes and values are lists of file paths.
    """
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return {}

    hash_to_paths = defaultdict(list)
    print(f"🎶 Initiating Echo Chamber Resonation in {directory}... 🎶")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath): # Skip symbolic links to avoid infinite loops or external files
                continue
            
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hash_to_paths[file_hash].append(filepath)
    
    return hash_to_paths

def report_duplicates(hash_to_paths):
    """
    Prints a report of all duplicate file groups found.
    """
    duplicate_groups = {h: paths for h, paths in hash_to_paths.items() if len(paths) > 1}

    if not duplicate_groups:
        print("\nNo echoing files found. Your chamber is uniquely resonant!")
        return

    print(f"\nFound {len(duplicate_groups)} groups of echoing files:")

    group_count = 1
    for file_hash, paths in duplicate_groups.items():
        print(f"\n--- Group {group_count} (SHA256: {file_hash[:12]}...) ---")
        for path in paths:
            print(f"  - {path}")
        group_count += 1
    
    print("\n🎶 Echo Chamber Resonation complete. Uniqueness amplified! 🎶")


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Resonator: Detects duplicate files in a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan for duplicate files."
    )

    args = parser.parse_args()

    hash_to_paths = find_duplicate_files(args.path)
    report_duplicates(hash_to_paths)

if __name__ == "__main__":
    main()
