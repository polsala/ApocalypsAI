import os
import sys
from collections import defaultdict

def format_bytes(size):
    """Formats a size in bytes to a human-readable string."""
    if size == 0:
        return "0.0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB" # Should be enough for most digital rubble

def audit_directory(path, top_n_largest=10):
    """Scans a directory and returns an asset audit report."""
    if not os.path.isdir(path):
        raise ValueError(f"Path '{path}' is not a valid directory.")

    file_counts = defaultdict(int)
    total_sizes = defaultdict(int)
    largest_files = [] # Stores (size, filepath) tuples
    total_files_scanned = 0
    total_size_scanned = 0

    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                size = os.path.getsize(filepath)
                total_files_scanned += 1
                total_size_scanned += size

                _, ext = os.path.splitext(file)
                ext = ext.lower() if ext else "(no_extension)"

                file_counts[ext] += 1
                total_sizes[ext] += size

                # Maintain top N largest files
                if len(largest_files) < top_n_largest:
                    largest_files.append((size, filepath))
                    largest_files.sort(key=lambda x: x[0], reverse=True)
                elif size > largest_files[-1][0]:
                    largest_files[-1] = (size, filepath)
                    largest_files.sort(key=lambda x: x[0], reverse=True)

            except OSError:
                # Skip files we can't access (e.g., permission errors, broken symlinks)
                pass

    report = {
        "scanned_path": path,
        "total_files_scanned": total_files_scanned,
        "total_size_scanned": total_size_scanned,
        "file_type_summary": {ext: {'count': file_counts[ext], 'size': total_sizes[ext]} for ext in sorted(file_counts.keys())},
        "largest_files": [{'path': f[1], 'size': f[0]} for f in largest_files]
    }
    return report

def print_report(report):
    """Prints the audit report in a human-readable format."""
    print(f"Asset Audit Report for: {report['scanned_path']}")
    print("-" * (len(report['scanned_path']) + 22))
    print(f"\nTotal Files Scanned: {report['total_files_scanned']}")
    print(f"Total Size Scanned: {format_bytes(report['total_size_scanned'])}")

    if report['file_type_summary']:
        print("\nFile Type Summary:")
        print("------------------")
        for ext, data in report['file_type_summary'].items():
            print(f"{ext:<15}: {data['count']} files ({format_bytes(data['size'])})")

    if report['largest_files']:
        print("\nTop Largest Files:")
        print("---------------------")
        for i, file_data in enumerate(report['largest_files']):
            print(f"{i+1}. {file_data['path']} ({format_bytes(file_data['size'])})")

    if not report['total_files_scanned']:
        print("\nNo files found in the specified directory.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 src/auditor.py <path_to_directory>", file=sys.stderr)
        sys.exit(1)

    target_path = sys.argv[1]
    try:
        audit_results = audit_directory(target_path)
        print_report(audit_results)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
