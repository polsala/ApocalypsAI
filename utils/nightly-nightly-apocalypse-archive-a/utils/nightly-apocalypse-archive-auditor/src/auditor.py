import os
import sys
from collections import defaultdict

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def audit_directory(path):
    """
    Scans a directory and its subdirectories, returning a summary of file types,
    counts, and total sizes.
    """
    if not os.path.isdir(path):
        print(f"Error: Directory not found at '{path}'", file=sys.stderr)
        sys.exit(1)

    file_stats = defaultdict(lambda: {'count': 0, 'size': 0})
    total_files = 0
    total_size_bytes = 0

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(file_path)
                _, ext = os.path.splitext(file_name)
                ext = ext.lower() if ext else "(No Ext)" # Handle files without extensions

                file_stats[ext]['count'] += 1
                file_stats[ext]['size'] += size
                total_files += 1
                total_size_bytes += size
            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}", file=sys.stderr)
                continue

    return file_stats, total_files, total_size_bytes

def print_report(path, file_stats, total_files, total_size_bytes):
    """Prints the formatted audit report."""
    print(f"\nApocalypse Archive Audit Report for: {path}")
    print("-" * 60)

    if not file_stats:
        print("No files found in the specified directory.")
        print("-" * 60)
        return

    # Sort by extension for consistent output
    sorted_stats = sorted(file_stats.items())

    max_ext_len = max(len(ext) for ext, _ in sorted_stats) if sorted_stats else 0
    if "(No Ext)" in file_stats: # Ensure (No Ext) is considered for padding
        max_ext_len = max(max_ext_len, len("(No Ext)"))

    for ext, stats in sorted_stats:
        formatted_size = format_size(stats['size'])
        print(f"{ext.ljust(max_ext_len)} | Count: {str(stats['count']).rjust(6)} | Size: {formatted_size.rjust(8)}")

    print("-" * 60)
    print(f"Total Files: {total_files}")
    print(f"Total Size: {format_size(total_size_bytes)}")
    print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python auditor.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    stats, total_files, total_size = audit_directory(target_directory)
    print_report(target_directory, stats, total_files, total_size)
