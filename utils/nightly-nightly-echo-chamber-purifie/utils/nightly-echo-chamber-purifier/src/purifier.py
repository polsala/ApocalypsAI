import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicate_files(paths):
    """
    Finds duplicate files in the given list of paths.
    Paths can be files or directories.
    """
    file_hashes = defaultdict(list)
    
    for path in paths:
        if os.path.isfile(path):
            file_hashes[calculate_file_hash(path)].append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    # Skip broken symlinks or unreadable files
                    if not os.path.islink(filepath) and os.path.exists(filepath):
                        file_hash = calculate_file_hash(filepath)
                        if file_hash: # Only add if hash was successfully calculated
                            file_hashes[file_hash].append(filepath)
        else:
            print(f"Warning: Path '{path}' is not a valid file or directory. Skipping.", file=sys.stderr)

    duplicates = {hash_val: files for hash_val, files in file_hashes.items() if len(files) > 1}
    return duplicates

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/purifier.py <directory1> [directory2 ...]")
        sys.exit(1)

    input_paths = sys.argv[1:]
    duplicates = find_duplicate_files(input_paths)

    if not duplicates:
        print("No duplicate files found. Your digital echo chamber is pristine!")
        sys.exit(0)

    print("--- Duplicate Files Found ---")
    for hash_val, files in duplicates.items():
        print(f"\nDuplicate Group (SHA256: {hash_val})")
        for filepath in files:
            print(f"  - {filepath}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
