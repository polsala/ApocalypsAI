import os
import sys
import argparse

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

def audit_directory(directory_path):
    """Scans a directory and returns an inventory of file types and sizes."""
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found or is not a directory.", file=sys.stderr)
        sys.exit(1)

    file_inventory = {}
    total_files = 0
    total_size_bytes = 0

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                size = os.path.getsize(file_path)
                _, ext = os.path.splitext(filename)
                ext = ext.lower() if ext else '(none)'

                file_inventory.setdefault(ext, {'count': 0, 'size': 0})
                file_inventory[ext]['count'] += 1
                file_inventory[ext]['size'] += size

                total_files += 1
                total_size_bytes += size
            except OSError as e:
                # Skip files we can't access, but log the error
                print(f"Warning: Could not access '{file_path}': {e}", file=sys.stderr)
                continue

    return file_inventory, total_files, total_size_bytes

def print_report(file_inventory, total_files, total_size_bytes, directory_path):
    """Prints a formatted report of the file inventory."""
    print(f"Scanning directory: {directory_path}")
    print("\n--- Asset Audit Report ---\n")

    print(f"Total Files: {total_files}")
    print(f"Total Size: {format_size(total_size_bytes)}\n")

    if not file_inventory:
        print("No files found in the directory.")
        return

    print("File Type Breakdown:")
    print("--------------------")

    # Sort by size descending for better readability
    sorted_inventory = sorted(file_inventory.items(), key=lambda item: item[1]['size'], reverse=True)

    for ext, data in sorted_inventory:
        count = data['count']
        size = data['size']
        percentage = (size / total_size_bytes * 100) if total_size_bytes > 0 else 0
        print(f"{ext:<5}: {count} file{'s' if count != 1 else ''} ({format_size(size)}) [{percentage:.1f}%]")
    print("--------------------")

def main():
    parser = argparse.ArgumentParser(
        description="Audit a directory for file types, counts, and total sizes."
    )
    parser.add_argument("directory_path", help="The path to the directory to audit.")
    args = parser.parse_args()

    file_inventory, total_files, total_size_bytes = audit_directory(args.directory_path)
    print_report(file_inventory, total_files, total_size_bytes, args.directory_path)

if __name__ == "__main__":
    main()
