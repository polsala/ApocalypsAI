import os
import hashlib
import argparse
from collections import defaultdict
import sys
import json

def calculate_file_hash(filepath, hash_algo='sha256', block_size=65536):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algo)
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except FileNotFoundError:
        return None
    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicate_files(paths, hash_algo='sha256', block_size=65536, min_size_kb=0):
    """
    Scans given paths for duplicate files based on their content hash.
    Returns a dictionary where keys are hashes and values are lists of file paths.
    """
    hashes = defaultdict(list)
    min_size_bytes = min_size_kb * 1024

    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: Path not found: {path}", file=sys.stderr)
            continue

        if os.path.isfile(path):
            if os.path.getsize(path) >= min_size_bytes:
                file_hash = calculate_file_hash(path, hash_algo, block_size)
                if file_hash:
                    hashes[file_hash].append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if os.path.isfile(filepath) and os.path.getsize(filepath) >= min_size_bytes:
                        file_hash = calculate_file_hash(filepath, hash_algo, block_size)
                        if file_hash:
                            hashes[file_hash].append(filepath)
    
    duplicates = {h: files for h, files in hashes.items() if len(files) > 1}
    return duplicates

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Purifier: Finds duplicate files in specified directories."
    )
    parser.add_argument(
        'paths',
        metavar='PATH',
        type=str,
        nargs='+',
        help='One or more file or directory paths to scan for duplicates.'
    )
    parser.add_argument(
        '--hash-algo',
        type=str,
        default='sha256',
        choices=hashlib.algorithms_available,
        help='Hashing algorithm to use (e.g., sha256, md5). Default: sha256.'
    )
    parser.add_argument(
        '--min-size-kb',
        type=int,
        default=0,
        help='Minimum file size in KB to consider for hashing. Files smaller than this will be ignored. Default: 0.'
    )
    parser.add_argument(
        '--output-format',
        type=str,
        default='text',
        choices=['text', 'json'],
        help='Output format for duplicates. Default: text.'
    )

    args = parser.parse_args()

    print(f"Scanning for duplicates in: {', '.join(args.paths)} (min size: {args.min_size_kb}KB, algo: {args.hash_algo})")
    duplicates = find_duplicate_files(args.paths, args.hash_algo, min_size_kb=args.min_size_kb)

    if not duplicates:
        print("No duplicate files found. The echo chamber is pure!")
        sys.exit(0)

    if args.output_format == 'json':
        print(json.dumps(duplicates, indent=2))
    else:
        print("\n--- Duplicate Files Found ---")
        for h, files in duplicates.items():
            print(f"Hash: {h}")
            for f in files:
                print(f"  - {f}")
            print("-" * 20)
    
    sys.exit(1) # Exit with 1 if duplicates are found, indicating action might be needed.

if __name__ == '__main__':
    main()
