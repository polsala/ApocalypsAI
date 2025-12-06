import os
import hashlib
import argparse
import sys

CHUNK_SIZE = 65536  # 64KB

def calculate_file_hash(filepath: str) -> str:
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return ""

def find_duplicates(root_dir: str) -> dict[str, list[str]]:
    """Finds duplicate files based on content hash."""
    file_hashes: dict[str, list[str]] = {}
    print(f"Scanning '{root_dir}' for files...")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.isfile(filepath):
                continue

            # Optimization: Skip files with size 0 or very small, or use size as a pre-filter
            # For simplicity, we'll hash all files for now.
            
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                file_hashes.setdefault(file_hash, []).append(filepath)
    
    # Filter out unique files (those with only one path)
    duplicates = {h: paths for h, paths in file_hashes.items() if len(paths) > 1}
    return duplicates

def link_duplicates(root_dir: str, dry_run: bool = False):
    """Replaces duplicate files with hard links to save space."""
    duplicates = find_duplicates(root_dir)

    if not duplicates:
        print("No duplicate files found. Disk space is optimally entangled!")
        return

    total_saved_space = 0
    total_linked_files = 0

    print(f"Found {sum(len(paths) - 1 for paths in duplicates.values())} potential duplicates across {len(duplicates)} unique file contents.")

    for file_hash, paths in duplicates.items():
        # The first file in the list will be the 'original' to link to
        original_file = paths[0]
        
        # Get original file size for calculating saved space
        try:
            original_size = os.path.getsize(original_file)
        except OSError as e:
            print(f"Warning: Could not get size of {original_file}: {e}. Skipping this group.", file=sys.stderr)
            continue

        print(f"\n--- Processing duplicates for hash {file_hash[:8]}... (Original: {original_file}) ---")

        for i in range(1, len(paths)): # Iterate through duplicates, skipping the original
            duplicate_file = paths[i]
            
            # Check if the file is already a hard link to the original (same inode)
            try:
                if os.stat(original_file).st_ino == os.stat(duplicate_file).st_ino:
                    print(f"  '{duplicate_file}' is already hard-linked to '{original_file}'. Skipping.")
                    continue
            except OSError as e:
                print(f"  Warning: Could not stat files {original_file} or {duplicate_file}: {e}. Proceeding with caution.", file=sys.stderr)
                # If stat fails, we can't reliably check inode, so proceed to remove/link attempt

            if dry_run:
                print(f"  [DRY RUN] Would remove '{duplicate_file}' and hard-link to '{original_file}'.")
                total_saved_space += original_size # Each duplicate removed saves its full size
                total_linked_files += 1
            else:
                try:
                    os.remove(duplicate_file)
                    os.link(original_file, duplicate_file)
                    print(f"  Removed '{duplicate_file}' and hard-linked to '{original_file}'.")
                    total_saved_space += original_size
                    total_linked_files += 1
                except OSError as e:
                    print(f"  Error processing '{duplicate_file}': {e}. Skipping.", file=sys.stderr)

    if dry_run:
        print(f"\n[DRY RUN SUMMARY] Would have linked {total_linked_files} files, saving approximately {total_saved_space / (1024*1024):.2f} MB.")
    else:
        print(f"\n[SUMMARY] Successfully linked {total_linked_files} files, saving approximately {total_saved_space / (1024*1024):.2f} MB.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Quantum Linker: Finds duplicate files and replaces them with hard links."
    )
    parser.add_argument(
        "--dir", 
        type=str, 
        required=True, 
        help="The root directory to scan for duplicate files."
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="If set, only report changes without modifying the file system."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Error: Directory '{args.dir}' not found or is not a directory.", file=sys.stderr)
        sys.exit(1)

    link_duplicates(args.dir, args.dry_run)

if __name__ == "__main__":
    main()
