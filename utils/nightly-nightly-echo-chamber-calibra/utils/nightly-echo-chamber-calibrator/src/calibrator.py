import os
import hashlib
import argparse
import sys

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file, reading it in blocks."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                block = f.read(block_size)
                if not block:
                    break
                hasher.update(block)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicates(paths, delete_duplicates=False, block_size=65536):
    """
    Scans specified paths for duplicate files based on SHA256 hash.
    Optionally deletes duplicates, keeping the first encountered instance.
    """
    file_hashes = {}
    all_files = []
    deleted_files = []

    print(f"Scanning {len(paths)} directories for files...")
    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.", file=sys.stderr)
            continue
        for root, _, files in os.walk(path):
            for filename in files:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    all_files.append(filepath)

    print(f"Found {len(all_files)} files. Calculating hashes...")
    for filepath in all_files:
        file_size = os.path.getsize(filepath)
        # Optimization: Group by size first to avoid hashing files of different sizes
        if file_size not in file_hashes:
            file_hashes[file_size] = {}
        
        current_size_group = file_hashes[file_size]
        file_hash = calculate_file_hash(filepath, block_size)
        
        if file_hash is None:
            continue # Error occurred during hashing

        if file_hash not in current_size_group:
            current_size_group[file_hash] = []
        current_size_group[file_hash].append(filepath)

    duplicates_found = 0
    print("\n--- Duplicate Report ---")
    for size_group in file_hashes.values():
        for file_hash, files in size_group.items():
            if len(files) > 1:
                duplicates_found += 1
                print(f"\nDuplicate Group (Hash: {file_hash[:10]}...):")
                for i, filepath in enumerate(files):
                    if i == 0:
                        print(f"  [KEEP] {filepath}")
                    else:
                        print(f"  [DUPE] {filepath}")
                        if delete_duplicates:
                            try:
                                os.remove(filepath)
                                deleted_files.append(filepath)
                                print(f"         Deleted: {filepath}")
                            except OSError as e:
                                print(f"         Error deleting {filepath}: {e}", file=sys.stderr)

    if duplicates_found == 0:
        print("No duplicate files found.")
    else:
        print(f"\n--- Summary ---")
        print(f"Total duplicate groups found: {duplicates_found}")
        if delete_duplicates:
            print(f"Total files deleted: {len(deleted_files)}")
        else:
            print("Run with --delete to remove duplicates (keeping one original).")
    
    return duplicates_found, deleted_files

def main():
    parser = argparse.ArgumentParser(
        description="Detect and optionally remove duplicate files based on SHA256 hash."
    )
    parser.add_argument(
        '--path', 
        action='append', 
        required=True, 
        help='Directory to scan for duplicate files. Can be specified multiple times.'
    )
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help='If specified, duplicates will be deleted (keeping one original). Use with caution!'
    )
    parser.add_argument(
        '--block-size', 
        type=int, 
        default=65536, 
        help='Block size in bytes for file hashing. Defaults to 65536 (64KB).'
    )

    args = parser.parse_args()

    if not args.path:
        parser.error("At least one --path argument is required.")

    if args.delete:
        confirm = input("WARNING: You are about to DELETE duplicate files. Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            sys.exit(0)

    duplicates_found, deleted_files = find_duplicates(args.path, args.delete, args.block_size)
    
    if duplicates_found > 0 and not args.delete:
        sys.exit(2) # Indicate duplicates found but not deleted (no-op for deletion)
    elif duplicates_found > 0 and args.delete and len(deleted_files) == 0:
        sys.exit(1) # Indicate failure if deletion was requested but nothing was deleted (e.g., permissions)
    elif duplicates_found == 0:
        sys.exit(0) # No duplicates, success
    else:
        sys.exit(0) # Duplicates found and deleted, success

if __name__ == '__main__':
    main()
