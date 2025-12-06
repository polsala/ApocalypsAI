import os
import argparse
from collections import defaultdict

def get_file_size_human_readable(size_bytes):
    """Convert a file size in bytes to a human-readable format."""
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(os.floor(os.log(size_bytes, 1024)))
    p = os.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def audit_directory(path, max_depth=None, top_n_largest=5):
    """
    Audits a directory, providing a summary of file types, counts, sizes,
    and the largest files.

    Args:
        path (str): The path to the directory to audit.
        max_depth (int, optional): Maximum recursion depth. None for unlimited.
        top_n_largest (int): Number of largest files to list.

    Returns:
        dict: A dictionary containing the audit report.
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directory not found: {path}")

    file_type_counts = defaultdict(int)
    file_type_sizes = defaultdict(int)
    all_files = []
    total_files = 0
    total_size = 0

    for root, dirs, files in os.walk(path):
        current_depth = root.count(os.sep) - path.count(os.sep)
        if max_depth is not None and current_depth > max_depth:
            del dirs[:] # Don't recurse into deeper directories
            continue

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                size = os.path.getsize(file_path)
                total_files += 1
                total_size += size
                extension = os.path.splitext(file_name)[1].lower() or "[no_extension]"
                
                file_type_counts[extension] += 1
                file_type_sizes[extension] += size
                all_files.append((size, file_path))
            except OSError:
                # Ignore files that cannot be accessed (e.g., broken symlinks)
                pass

    # Sort files by size in descending order
    all_files.sort(key=lambda x: x[0], reverse=True)

    report = {
        "summary": {
            "total_files": total_files,
            "total_size": get_file_size_human_readable(total_size),
            "total_size_bytes": total_size,
            "audited_path": os.path.abspath(path)
        },
        "file_types": {},
        "largest_files": []
    }

    for ext, count in sorted(file_type_counts.items(), key=lambda item: item[1], reverse=True):
        size = file_type_sizes[ext]
        report["file_types"][ext] = {
            "count": count,
            "size": get_file_size_human_readable(size),
            "size_bytes": size
        }

    for size, file_path in all_files[:top_n_largest]:
        report["largest_files"].append({
            "path": file_path,
            "size": get_file_size_human_readable(size),
            "size_bytes": size
        })

    return report

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse Archive Auditor: Scan directories for file type summaries and largest files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The path to the directory you want to audit."
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=None,
        help="Maximum recursion depth. 0 for current directory only, 1 for current + immediate subdirectories, etc. Default is unlimited."
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=5,
        help="Number of largest files to list. Default is 5."
    )

    args = parser.parse_args()

    try:
        report = audit_directory(args.path, args.depth, args.top_n)
        print(f"--- Apocalypse Archive Audit Report for: {report['summary']['audited_path']} ---")
        print(f"Total Files: {report['summary']['total_files']}")
        print(f"Total Size: {report['summary']['total_size']}")
        print("\n--- File Type Breakdown ---")
        if not report["file_types"]:
            print("No files found.")
        for ext, data in report["file_types"].items():
            print(f"  {ext:<15}: {data['count']:<5} files, {data['size']}")

        print(f"\n--- Top {len(report['largest_files'])} Largest Files ---")
        if not report["largest_files"]:
            print("No files found.")
        for item in report["largest_files"]:
            print(f"  {item['size']:<10} - {item['path']}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
