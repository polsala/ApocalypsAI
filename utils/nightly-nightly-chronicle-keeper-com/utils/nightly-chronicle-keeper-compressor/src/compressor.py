import os
import hashlib
import argparse
import sys

def get_file_hash(filepath, block_size=65536):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except IOError:
        return None

def scan_directory(path, min_size_for_large):
    """Scans a directory for duplicates, large files, and empty files.

    Args:
        path (str): The root directory to scan.
        min_size_for_large (int): Minimum size in bytes for a file to be considered large.

    Returns:
        tuple: (duplicates, large_files, empty_files, total_files, total_size)
            duplicates (dict): {hash: [filepath1, filepath2, ...]}.
            large_files (list): List of (filepath, size) for large files.
            empty_files (list): List of filepaths for empty files.
            total_files (int): Total number of files scanned.
            total_size (int): Total size in bytes of all files scanned.
    """
    file_hashes = {}
    large_files = []
    empty_files = []
    total_files = 0
    total_size = 0

    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if not os.path.islink(filepath) and os.path.isfile(filepath):
                try:
                    size = os.path.getsize(filepath)
                    total_files += 1
                    total_size += size

                    if size == 0:
                        empty_files.append(filepath)

                    if size > min_size_for_large:
                        large_files.append((filepath, size))

                    file_hash = get_file_hash(filepath)
                    if file_hash:
                        file_hashes.setdefault(file_hash, []).append(filepath)

                except (OSError, IOError) as e:
                    print(f"Warning: Could not access {filepath} - {e}", file=sys.stderr)

    # Filter out hashes that only appeared once (not duplicates)
    duplicates = {h: paths for h, paths in file_hashes.items() if len(paths) > 1}

    return duplicates, large_files, empty_files, total_files, total_size

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(os.path.floor(os.path.log(size_bytes, 1024)))
    p = pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def generate_report(duplicates, large_files, empty_files, total_files, total_size):
    """Prints a summary report of the scan findings."""
    print("\n--- Chronicle Keeper's Content Compressor Report ---")
    print(f"Scanned {total_files} files, totaling {format_size(total_size)}.\n")

    if duplicates:
        print("### Duplicate Files Found ###")
        print("The following files have identical content. Consider deleting the redundant copies:")
        for file_hash, paths in duplicates.items():
            print(f"  Hash: {file_hash}")
            for p in paths:
                print(f"    - {p}")
        print(f"Total duplicate groups: {len(duplicates)}\n")
    else:
        print("No duplicate files found.\n")

    if large_files:
        print("### Large Files Found ###")
        print("The following files exceed the configured size threshold. Review them for potential compression or archiving:")
        # Sort large files by size, descending
        large_files.sort(key=lambda x: x[1], reverse=True)
        for filepath, size in large_files:
            print(f"  - {filepath} ({format_size(size)})")
        print(f"Total large files: {len(large_files)}\n")
    else:
        print("No excessively large files found.\n")

    if empty_files:
        print("### Empty Files Found ###")
        print("The following files are empty (0 bytes). They can likely be safely deleted:")
        for filepath in empty_files:
            print(f"  - {filepath}")
        print(f"Total empty files: {len(empty_files)}\n")
    else:
        print("No empty files found.\n")

    print("--- End of Report ---")

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle Keeper's Content Compressor: Identify and report on redundant, large, or empty files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=104857600, # Default to 100 MB
        help="Minimum size (in bytes) for a file to be considered 'large'. Default: 104857600 (100 MB)."
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="If present, the utility will only print the report and not attempt any interactive actions."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The provided path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning directory: {args.path}...")
    duplicates, large_files, empty_files, total_files, total_size = scan_directory(args.path, args.min_size)
    generate_report(duplicates, large_files, empty_files, total_files, total_size)

    # The --report-only flag is currently a placeholder as no interactive actions are implemented.
    # Future expansion could include interactive deletion/compression suggestions.

if __name__ == "__main__":
    main()
