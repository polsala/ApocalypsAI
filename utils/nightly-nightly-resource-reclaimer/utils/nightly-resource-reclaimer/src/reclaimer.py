import os
import hashlib
import sys

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None # Handle unreadable files gracefully

def find_duplicates_and_empty_dirs(root_path):
    """Finds duplicate files and empty directories within a given root_path.

    Returns a tuple: (dict of {hash: [filepaths]}, list of empty_dir_paths, total_potential_reclaim_size_bytes)
    """
    file_hashes = {}
    empty_dirs = []
    total_potential_reclaim_size = 0

    for dirpath, dirnames, filenames in os.walk(root_path):
        # Check for empty directories *after* processing files in this dir
        # and before recursing into subdirectories. An empty dir is one
        # with no files AND no subdirectories.
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not os.path.islink(filepath) and os.path.isfile(filepath):
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    if file_hash not in file_hashes:
                        file_hashes[file_hash] = []
                    file_hashes[file_hash].append(filepath)

    duplicates = {h: paths for h, paths in file_hashes.items() if len(paths) > 1}

    # Calculate potential reclaim size from duplicates
    for h, paths in duplicates.items():
        if paths:
            # Size of the first file, multiplied by (number of duplicates - 1)
            # as one copy is kept.
            try:
                total_potential_reclaim_size += os.path.getsize(paths[0]) * (len(paths) - 1)
            except OSError:
                pass # File might have been deleted or inaccessible

    return duplicates, empty_dirs, total_potential_reclaim_size

def main():
    if len(sys.argv) < 2:
        print("Usage: python reclaimer.py <path_to_scan>")
        sys.exit(1)

    root_path = sys.argv[1]

    if not os.path.isdir(root_path):
        print(f"Error: '{root_path}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning {root_path}...")

    duplicates, empty_dirs, potential_reclaim_size = find_duplicates_and_empty_dirs(root_path)

    print("\n--- Duplicate Files Found ---")
    if duplicates:
        for i, (file_hash, paths) in enumerate(duplicates.items()):
            print(f"\nGroup {i+1} (MD5: {file_hash}):")
            for p in paths:
                try:
                    size_kb = os.path.getsize(p) / 1024
                    print(f"  - {p} ({size_kb:.0f} KB)")
                except OSError:
                    print(f"  - {p} (Inaccessible)")
    else:
        print("No duplicate files found.")

    print("\n--- Empty Directories Found ---")
    if empty_dirs:
        for d in empty_dirs:
            print(f"  - {d}/")
    else:
        print("No empty directories found.")

    print(f"\nScan complete. Reclaimed potential: {potential_reclaim_size / 1024:.0f} KB (from duplicates) + {len(empty_dirs)} empty directories.")

if __name__ == '__main__':
    main()
