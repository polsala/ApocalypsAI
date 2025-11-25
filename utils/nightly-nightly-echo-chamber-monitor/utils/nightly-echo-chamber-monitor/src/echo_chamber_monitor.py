import os
import hashlib
import argparse
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algo='sha256', chunk_size=4096):
    """Calculates the hash of a file."""
    hasher = hashlib.new(hash_algo)
    try:
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError:
        return None # File might be inaccessible or not exist

def find_duplicate_files(paths, min_size=1):
    """
    Finds duplicate files in the given paths.

    Args:
        paths (list): A list of directory paths to scan.
        min_size (int): Minimum file size in bytes to consider for hashing.

    Returns:
        dict: A dictionary where keys are file hashes and values are lists of file paths
              that share that hash, but only for hashes with more than one file.
    """
    files_by_size = defaultdict(list)
    for path in paths:
        if not os.path.isdir(path):
            print(f"Warning: Path '{path}' is not a valid directory. Skipping.", file=sys.stderr)
            continue

        for root, _, filenames in os.walk(path):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                try:
                    # Skip symlinks to avoid infinite loops or external files
                    if os.path.islink(filepath):
                        continue
                    
                    file_size = os.path.getsize(filepath)
                    if file_size >= min_size:
                        files_by_size[file_size].append(filepath)
                except (OSError, FileNotFoundError):
                    # File might have been deleted between os.walk and os.path.getsize
                    continue

    duplicates = defaultdict(list)
    for size, filepaths in files_by_size.items():
        if len(filepaths) < 2: # No duplicates if only one file of this size
            continue

        # For files of the same size, calculate hash to find true duplicates
        files_by_hash = defaultdict(list)
        for filepath in filepaths:
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                files_by_hash[file_hash].append(filepath)
        
        for file_hash, paths_with_same_hash in files_by_hash.items():
            if len(paths_with_same_hash) > 1:
                duplicates[file_hash].extend(paths_with_same_hash)
    
    return duplicates

def generate_report(duplicates, output_file=None):
    """
    Generates a report of duplicate files.

    Args:
        duplicates (dict): Dictionary of duplicate files.
        output_file (str, optional): Path to write the report. If None, prints to stdout.
    """
    if not duplicates:
        report_content = "No duplicate files found. The void is clear! ✨"
    else:
        report_lines = ["--- Duplicate Files Found ---"]
        group_num = 1
        for file_hash, filepaths in duplicates.items():
            report_lines.append(f"\nGroup {group_num} (SHA256: {file_hash})")
            for filepath in sorted(filepaths): # Sort for deterministic output
                report_lines.append(f"  - {filepath}")
            group_num += 1
        report_lines.append("\n--- End of Report ---")
        report_content = "\n".join(report_lines)

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(report_content)
            print(f"Report written to {output_file}")
        except IOError as e:
            print(f"Error writing report to {output_file}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report_content)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echo Chamber Monitor: Finds and reports duplicate files."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="One or more paths to directories to scan for duplicates. Can be provided multiple times."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=1,
        help="Minimum file size (in bytes) to consider for hashing. Files smaller than this will be ignored. Defaults to 1 byte (i.e., ignores empty files)."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional. Path to a file where the report will be written. If not provided, the report is printed to stdout."
    )

    args = parser.parse_args()

    if not args.path:
        parser.error("At least one --path argument is required.")

    duplicates = find_duplicate_files(args.path, args.min_size)
    generate_report(duplicates, args.output)

if __name__ == "__main__":
    main()
