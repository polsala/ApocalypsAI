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
    except IOError as e:
        raise IOError(f"Could not read file '{filepath}': {e}")
    return sha256.hexdigest()

def find_duplicate_files(directories):
    """
    Scans specified directories for files and groups them by their SHA256 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    hash_to_files = defaultdict(list)
    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory '{directory}' not found or is not a directory. Skipping.")
            continue
        for root, _, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                try:
                    # Skip symbolic links to avoid infinite loops or issues with target files
                    if os.path.islink(filepath):
                        continue
                    file_hash = calculate_file_hash(filepath)
                    hash_to_files[file_hash].append(filepath)
                except IOError as e:
                    print(f"Error processing file '{filepath}': {e}")
                except Exception as e:
                    print(f"An unexpected error occurred with file '{filepath}': {e}")
    return {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}

def harmonize_duplicates(duplicate_groups, dry_run=True):
    """
    Replaces duplicate files with hard links to a single master file.
    """
    total_saved_space = 0
    total_files_linked = 0

    for file_hash, file_paths in duplicate_groups.items():
        master_file = file_paths[0]
        print(f"\nHash: {file_hash[:10]}... (Master: {master_file})")
        for i, duplicate_file in enumerate(file_paths[1:]): # Skip the master file
            if os.path.samefile(master_file, duplicate_file):
                print(f"  Skipping '{duplicate_file}' - already hardlinked to master.")
                continue

            try:
                original_size = os.path.getsize(duplicate_file)
                if dry_run:
                    print(f"  [DRY RUN] Would replace '{duplicate_file}' with a hard link to '{master_file}'. (Potential save: {original_size} bytes)")
                else:
                    os.remove(duplicate_file) # Remove the duplicate
                    os.link(master_file, duplicate_file) # Create a hard link
                    print(f"  Replaced '{duplicate_file}' with a hard link to '{master_file}'. (Saved: {original_size} bytes)")
                    total_saved_space += original_size
                    total_files_linked += 1
            except OSError as e:
                print(f"  Error processing '{duplicate_file}': {e}")
            except Exception as e:
                print(f"  An unexpected error occurred with '{duplicate_file}': {e}")

    if dry_run:
        print("\n--- DRY RUN COMPLETE ---")
        print("No changes were made to the file system.")
    else:
        print("\n--- HARMONIZATION COMPLETE ---")
        print(f"Total files linked: {total_files_linked}")
        print(f"Total potential space saved: {total_saved_space} bytes")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Data Harmonizer: Untangling the Quantum Duplicates. "
                    "Scans directories for duplicate files by content hash and replaces them with hard links to save disk space."
    )
    parser.add_argument(
        'directories',
        metavar='DIR',
        nargs='+',
        help='One or more directories to scan for duplicate files.'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without making any changes to the file system.'
    )
    args = parser.parse_args()

    print("Nightly Data Harmonizer: Initiating Quantum Duplicate Scan...")
    print(f"Scanning directories: {', '.join(args.directories)}")
    print(f"Mode: {'Dry Run' if args.dry_run else 'Live Harmonization'}")

    duplicate_groups = find_duplicate_files(args.directories)

    if not duplicate_groups:
        print("\nNo quantum duplicates detected. Your data is already harmonized!")
        return

    print(f"\nDetected {len(duplicate_groups)} groups of quantum duplicates.")
    harmonize_duplicates(duplicate_groups, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
