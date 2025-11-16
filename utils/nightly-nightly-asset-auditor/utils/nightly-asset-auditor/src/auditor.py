import os
import argparse
from collections import defaultdict

def audit_directory(path):
    """
    Scans a directory, counts files by extension, and calculates total size.

    Args:
        path (str): The path to the directory to audit.

    Returns:
        dict: A dictionary containing the audit summary:
              - 'total_files': int
              - 'total_size_bytes': int
              - 'files_by_extension': dict (e.g., {'.py': 5, '.md': 2})
              - 'empty_files': int
    """
    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a valid directory.")

    total_files = 0
    total_size_bytes = 0
    files_by_extension = defaultdict(int)
    empty_files = 0

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            total_files += 1

            try:
                file_size = os.path.getsize(file_path)
                total_size_bytes += file_size
                if file_size == 0:
                    empty_files += 1
            except OSError:
                # Handle cases where file might be inaccessible or disappear during walk
                pass

            _, ext = os.path.splitext(file_name)
            files_by_extension[ext.lower()] += 1

    return {
        'total_files': total_files,
        'total_size_bytes': total_size_bytes,
        'files_by_extension': dict(files_by_extension),
        'empty_files': empty_files,
    }

def format_size(size_bytes):
    """Formats bytes into human-readable string."""
    if size_bytes == 0:
        return "0 B"
    size_names = ("B", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse Asset Auditor: Scans a directory and provides a summary of its contents."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to audit."
    )
    args = parser.parse_args()

    try:
        summary = audit_directory(args.directory)
        print(f"--- Asset Audit Report for: {args.directory} ---")
        print(f"Total Files: {summary['total_files']}")
        print(f"Total Size: {format_size(summary['total_size_bytes'])}")
        print("\nFiles by Extension:")
        if summary['files_by_extension']:
            for ext, count in sorted(summary['files_by_extension'].items()):
                print(f"  {ext if ext else '[no extension]'}: {count}")
        else:
            print("  No files with extensions found.")
        print(f"\nEmpty Files: {summary['empty_files']}")
        print("---------------------------------------")
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
