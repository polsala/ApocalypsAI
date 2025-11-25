import os
import hashlib
import argparse
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                sha256.update(block)
        return sha256.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def get_file_info(directory):
    """Walks a directory and collects file paths, sizes, and hashes."""
    file_info = []
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath):
                try:
                    size = os.path.getsize(filepath)
                    file_info.append({
                        'path': filepath,
                        'size': size,
                        'hash': None # Hash will be calculated only if needed for duplicates
                    })
                except OSError: # e.g., file disappeared or permission denied
                    pass
    return file_info

def find_empty_files(file_info):
    """Finds files with 0 bytes."""
    return [f['path'] for f in file_info if f['size'] == 0]

def find_large_files(file_info, max_size_bytes):
    """Finds files exceeding a specified size."""
    return [{'path': f['path'], 'size_mb': round(f['size'] / (1024 * 1024), 2)} 
            for f in file_info if f['size'] > max_size_bytes]

def find_duplicate_files(file_info):
    """Finds files with identical content using SHA256 hashes."""
    hash_map = defaultdict(list)
    for f in file_info:
        # Only calculate hash if file is not empty and not already processed
        if f['size'] > 0:
            file_hash = calculate_file_hash(f['path'])
            if file_hash:
                hash_map[file_hash].append(f['path'])
    
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Validate a 'scavenger's stash' directory for empty, large, and duplicate files."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The path to the directory to validate.'
    )
    parser.add_argument(
        '--max-size', 
        type=int, 
        default=100, 
        help='Maximum allowed file size in megabytes. Files larger than this will be flagged. (Default: 100 MB)'
    )

    args = parser.parse_args()
    target_directory = args.path
    max_size_mb = args.max_size
    max_size_bytes = max_size_mb * 1024 * 1024

    if not os.path.isdir(target_directory):
        print(f"Error: Directory '{target_directory}' not found or is not a directory.")
        exit(1)

    print(f"Scanning {target_directory}...")
    all_file_info = get_file_info(target_directory)

    empty_files = find_empty_files(all_file_info)
    large_files = find_large_files(all_file_info, max_size_bytes)
    duplicate_files = find_duplicate_files(all_file_info)

    print("\n--- Stash Validation Report ---")

    total_issues = 0

    if empty_files:
        print("\n[!] Found {} empty files:".format(len(empty_files)))
        for f in empty_files:
            print(f"    - {f}")
        total_issues += len(empty_files)
    
    if large_files:
        print("\n[!] Found {} large files (exceeds {} MB):".format(len(large_files), max_size_mb))
        for f in large_files:
            print(f"    - {f['path']} ({f['size_mb']} MB)")
        total_issues += len(large_files)

    if duplicate_files:
        print("\n[!] Found {} sets of duplicate files:".format(len(duplicate_files)))
        group_num = 1
        for file_hash, paths in duplicate_files.items():
            print(f"    - Group {group_num} (SHA256: {file_hash[:10]}...):")
            for p in paths:
                print(f"        - {p}")
            group_num += 1
        total_issues += len(duplicate_files)

    if not empty_files and not large_files and not duplicate_files:
        print("\n[✓] No issues found. Your stash is pristine!")

    print("\n--- Scan Complete ---")
    print(f"Total files scanned: {len(all_file_info)}")
    print(f"Total issues found: {total_issues}")


if __name__ == '__main__':
    main()
