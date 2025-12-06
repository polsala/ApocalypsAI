import os
import time
import hashlib
import argparse
from collections import defaultdict

def get_file_hash(filepath, block_size=65536):
    """Generates a SHA256 hash for a given file."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def scan_directory(path, age_days, size_mb, detect_duplicates):
    """
    Scans a directory for old, large, and duplicate files.

    Args:
        path (str): The directory to scan.
        age_days (int): Files older than this many days are reported.
        size_mb (int): Files larger than this many MB are reported.
        detect_duplicates (bool): If True, detect duplicate files by hash.

    Returns:
        dict: A dictionary containing lists of 'old_files', 'large_files', and 'duplicate_files'.
    """
    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a valid directory.")

    current_time = time.time()
    age_threshold_seconds = age_days * 24 * 60 * 60
    size_threshold_bytes = size_mb * 1024 * 1024

    old_files = []
    large_files = []
    file_hashes = defaultdict(list) # hash -> [filepath1, filepath2, ...]

    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                # Use os.path.getmtime for last modification time
                # For creation time, os.path.getctime might be used, but mtime is more common for "old" files.
                file_mtime = os.path.getmtime(filepath);
                file_size = os.path.getsize(filepath);

                if (current_time - file_mtime) > age_threshold_seconds:
                    old_files.append((filepath, file_mtime))

                if file_size > size_threshold_bytes:
                    large_files.append((filepath, file_size))

                if detect_duplicates:
                    file_hashes[get_file_hash(filepath)].append(filepath)

            except OSError as e:
                print(f"Warning: Could not process {filepath}: {e}")
                continue

    duplicate_files = []
    if detect_duplicates:
        for file_hash, paths in file_hashes.items():
            if len(paths) > 1:
                duplicate_files.append((file_hash, paths))

    return {
        'old_files': sorted(old_files, key=lambda x: x[1]),
        'large_files': sorted(large_files, key=lambda x: x[1], reverse=True),
        'duplicate_files': duplicate_files
    }

def generate_report(results, output_file=None):
    """Generates a human-readable report from the scan results."""
    report_lines = []
    report_lines.append("--- Gloom-and-Doom Data Duster Report ---")
    report_lines.append(f"Scan Date: {time.ctime(time.time())}\n")

    if results['old_files']:
        report_lines.append("### Ancient Artifacts (Older than threshold):")
        for filepath, mtime in results['old_files']:
            report_lines.append(f"- {filepath} (Last modified: {time.ctime(mtime)})")
        report_lines.append("")
    else:
        report_lines.append("No ancient artifacts found. Your digital history is surprisingly fresh!\n")

    if results['large_files']:
        report_lines.append("### Bloated Behemoths (Larger than threshold):")
        for filepath, size in results['large_files']:
            report_lines.append(f"- {filepath} ({size / (1024*1024):.2f} MB)")
        report_lines.append("")
    else:
        report_lines.append("No bloated behemoths found. Your files are lean and mean!\n")

    if results['duplicate_files']:
        report_lines.append("### Insidious Duplicates (Identical content):")
        for file_hash, paths in results['duplicate_files']:
            report_lines.append(f"  Hash: {file_hash[:10]}...")
            for p in paths:
                report_lines.append(f"    - {p}")
            report_lines.append("")
        report_lines.append("")
    else:
        report_lines.append("No insidious duplicates found. Your data is unique!\n")

    report_lines.append("--- End of Report ---")

    report_content = "\n".join(report_lines)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(report_content)
        print(f"Report saved to {output_file}")
    else:
        print(report_content)

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-and-Doom Data Duster: Reclaim your digital wasteland by finding old, large, and duplicate files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=365,
        help="Report files older than this many days. Default: 365 (1 year)."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=100,
        help="Report files larger than this many megabytes. Default: 100 MB."
    )
    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="Enable duplicate file detection based on content hash. Can be CPU intensive."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Save the report to a specified file instead of printing to console."
    )

    args = parser.parse_args()

    try:
        print(f"Scanning '{args.path}' for digital rubble...")
        results = scan_directory(args.path, args.age, args.size, args.duplicates)
        generate_report(results, args.output)
        print("Scan complete. May your storage be ever spacious!")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
