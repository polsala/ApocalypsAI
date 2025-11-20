import os
import sys
from collections import defaultdict

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(os.path.floor(os.path.log(size_bytes, 1024)))
    p = os.path.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def audit_directory(root_dir):
    """Scans a directory and its subdirectories, returning a summary report."""
    if not os.path.isdir(root_dir):
        return f"Error: Directory '{root_dir}' not found or is not a directory."

    file_counts = defaultdict(int)
    file_sizes = defaultdict(int)
    total_files = 0
    total_size_bytes = 0

    # Directories to ignore (common development/system directories)
    ignore_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'env', '.idea', '.vscode', 'build', 'dist'}

    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Modify dirs in-place to prune directories from further traversal
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                _, ext = os.path.splitext(file)
                ext = ext.lower() if ext else '(no ext)'

                file_counts[ext] += 1
                file_sizes[ext] += size
                total_files += 1
                total_size_bytes += size
            except OSError: # e.g., file disappeared between os.walk and os.path.getsize
                continue

    report_lines = []
    report_lines.append(f"Apocalypse Asset Audit Report for: {root_dir}")
    report_lines.append("-" * (len(report_lines[0])))
    report_lines.append("")
    report_lines.append(f"Total Files Scanned: {total_files}")
    report_lines.append(f"Total Size: {format_size(total_size_bytes)}")
    report_lines.append("")
    report_lines.append("File Type Summary:")
    report_lines.append("")

    if not file_counts:
        report_lines.append("No files found matching criteria.")
    else:
        # Sort by count descending, then by size descending
        sorted_extensions = sorted(
            file_counts.keys(),
            key=lambda ext: (file_counts[ext], file_sizes[ext]),
            reverse=True
        )

        # Determine max widths for formatting
        max_ext_len = max(len(ext) for ext in sorted_extensions) if sorted_extensions else len("Extension")
        max_count_len = max(len(str(file_counts[ext])) for ext in sorted_extensions) if sorted_extensions else len("Count")
        max_size_len = max(len(format_size(file_sizes[ext])) for ext in sorted_extensions) if sorted_extensions else len("Total Size")

        # Ensure header is at least as wide as content
        max_ext_len = max(max_ext_len, len("Extension"))
        max_count_len = max(max_count_len, len("Count"))
        max_size_len = max(max_size_len, len("Total Size"))

        header = f"| {'Extension':<{max_ext_len}} | {'Count':<{max_count_len}} | {'Total Size':<{max_size_len}} |"
        separator = f"|:{'-' * (max_ext_len - 1)} |:{'-' * (max_count_len - 1)} |:{'-' * (max_size_len - 1)} |"
        report_lines.append(header)
        report_lines.append(separator)

        for ext in sorted_extensions:
            count = file_counts[ext]
            size = file_sizes[ext]
            report_lines.append(
                f"| {ext:<{max_ext_len}} | {count:<{max_count_len}} | {format_size(size):<{max_size_len}} |"
            )

    report_lines.append("-" * (len(report_lines[1])))
    report_lines.append("Audit Complete. May your digital assets be ever in your favor.")

    return "\n".join(report_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auditor.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]
    report = audit_directory(target_directory)
    print(report)
