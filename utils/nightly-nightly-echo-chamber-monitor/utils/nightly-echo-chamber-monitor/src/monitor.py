import os
import hashlib
import argparse
import sys

def calculate_file_hash(filepath, block_size=65536):
    """Calculates the SHA256 hash of a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    """
    Scans a directory for duplicate files based on their SHA256 hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    Only includes hashes that have more than one associated file path (i.e., duplicates).
    """
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    hashes = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                file_hash = calculate_file_hash(filepath)
                if file_hash not in hashes:
                    hashes[file_hash] = []
                hashes[file_hash].append(filepath)
            except FileNotFoundError:
                # File might have been deleted between os.walk and hash calculation
                print(f"Warning: File disappeared during scan: {filepath}", file=sys.stderr)
            except Exception as e:
                print(f"Error processing file {filepath}: {e}", file=sys.stderr)

    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Echo Chamber Monitor: Finds duplicate files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for duplicate files."
    )
    args = parser.parse_args()

    try:
        duplicates = find_duplicate_files(args.directory)

        if duplicates:
            print("Found duplicate files:")
            for file_hash, paths in duplicates.items():
                print(f"  Hash: {file_hash}")
                for path in paths:
                    print(f"    - {path}")
        else:
            print("No duplicate files found.")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except NotADirectoryError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
