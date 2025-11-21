import os
import hashlib
import sys
from collections import defaultdict

def find_empty_directories(root_dir):
    """
    Finds all empty directories within a given root directory.
    A directory is considered empty if it contains no files and no subdirectories.
    """
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs

def calculate_file_hash(filepath, hash_algo=hashlib.sha256):
    """
    Calculates the SHA256 hash of a file.
    """
    hasher = hash_algo()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192): # Read in 8KB chunks
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files
    except Exception:
        return None # Catch other potential errors

def find_duplicate_files(root_dir):
    """
    Finds duplicate files within a given root directory based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    hashes = defaultdict(list)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.islink(filepath): # Skip symbolic links
                continue
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes[file_hash].append(filepath)

    duplicate_groups = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicate_groups

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/detector.py <directory_to_scan>")
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning {target_dir} for digital dust bunnies...\n")

    # Find empty directories
    empty_dirs = find_empty_directories(target_dir)
    if empty_dirs:
        print("--- Empty Directories Found ---")
        for d in empty_dirs:
            print(f"- {d}")
    else:
        print("No empty directories found. Good job! 👍")
    print()

    # Find duplicate files
    duplicate_files = find_duplicate_files(target_dir)
    if duplicate_files:
        print("--- Duplicate Files Found ---")
        group_num = 1
        for file_hash, paths in duplicate_files.items():
            print(f"- Group {group_num} (SHA256: {file_hash[:10]}...)")
            for p in paths:
                print(f"  - {p}")
            group_num += 1
    else:
        print("No duplicate files found. Your files are unique! ✨")
    print("\nScan complete. Time to sweep! 🧹")

if __name__ == "__main__":
    main()
