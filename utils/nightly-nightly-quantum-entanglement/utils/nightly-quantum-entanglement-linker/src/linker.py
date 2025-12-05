import os
import hashlib
from collections import defaultdict

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hasher.update(block)
    return hasher.hexdigest()

def find_and_link_duplicates(directory):
    """
    Finds duplicate files in the given directory and replaces them with hard links.
    Returns a tuple: (list of linked files, total bytes saved).
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")

    file_hashes = defaultdict(list)
    linked_files = []
    bytes_saved = 0

    print(f"Scanning '{directory}' for duplicate files...")
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hash = calculate_file_hash(filepath)
                file_hashes[file_hash].append(filepath)
            except IOError as e:
                print(f"Warning: Could not read file {filepath} - {e}")
                continue

    print("Identifying duplicates and creating hard links...")
    for file_hash, paths in file_hashes.items():
        if len(paths) > 1:
            # Sort paths to ensure deterministic "master" file selection
            # For simplicity, pick the first one as the master.
            master_file = paths[0]
            master_size = os.path.getsize(master_file)

            for i in range(1, len(paths)):
                duplicate_file = paths[i]
                try:
                    # Remove the duplicate
                    os.remove(duplicate_file)
                    # Create a hard link to the master file
                    os.link(master_file, duplicate_file)
                    linked_files.append((duplicate_file, master_file))
                    bytes_saved += master_size # Each duplicate removed saves its size
                    print(f"  Linked '{duplicate_file}' to '{master_file}'")
                except OSError as e:
                    print(f"Error linking '{duplicate_file}' to '{master_file}': {e}")

    return linked_files, bytes_saved

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Nightly Quantum Entanglement Linker: Finds duplicate files and replaces them with hard links."
    )
    parser.add_argument("directory", help="The directory to scan for duplicate files.")
    args = parser.parse_args()

    try:
        linked_files, bytes_saved = find_and_link_duplicates(args.directory)
        if linked_files:
            print(f"\nSuccessfully linked {len(linked_files)} duplicate files.")
            print(f"Total disk space saved: {bytes_saved / (1024*1024):.2f} MB")
        else:
            print("\nNo duplicate files found or linked.")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
