import os
import argparse
from collections import defaultdict

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def audit_directory(directory_path, allowed_extensions=None, critical_keywords=None):
    """
    Scans a directory for files, categorizes them by extension,
    calculates total size, and identifies files with critical keywords.
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    file_counts = defaultdict(int)
    file_sizes = defaultdict(int)
    critical_files = defaultdict(list)
    total_files_scanned = 0
    total_size_scanned = 0

    if critical_keywords:
        critical_keywords_lower = [k.lower() for k in critical_keywords]
    else:
        critical_keywords_lower = []

    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            _, ext = os.path.splitext(filename)
            ext = ext.lower() # Ensure consistent extension casing

            if allowed_extensions and ext not in allowed_extensions:
                continue

            total_files_scanned += 1
            try:
                file_size = os.path.getsize(file_path)
                total_size_scanned += file_size
                file_counts[ext] += 1
                file_sizes[ext] += file_size
            except OSError:
                # Handle cases where file might be inaccessible or broken symlink
                continue

            if critical_keywords_lower:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        found_keywords = [
                            kw for kw in critical_keywords_lower if kw in content
                        ]
                        if found_keywords:
                            critical_files[file_path].extend(found_keywords)
                except (IOError, UnicodeDecodeError):
                    # Skip binary files or unreadable text files for keyword search
                    pass

    report = []
    report.append(f"--- Asset Audit Report for '{directory_path}' ---")
    report.append(f"Total files scanned: {total_files_scanned}")
    report.append(f"Total size scanned: {format_size(total_size_scanned)}")
    report.append("\n--- File Type Summary ---")

    if not file_counts:
        report.append("No files found matching criteria.")
    else:
        for ext in sorted(file_counts.keys()):
            count = file_counts[ext]
            size = file_sizes[ext]
            report.append(f"  {ext}: {count} files, {format_size(size)}")

    if critical_files:
        report.append("\n--- Critical Files Found ---")
        for file_path, keywords in sorted(critical_files.items()):
            report.append(f"  - {file_path} (Keywords: {', '.join(set(keywords))})")
    else:
        report.append("\nNo critical files found.")

    report.append("\n--- End of Report ---")
    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description="Audits a directory for file types and critical keywords."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The root directory to scan."
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=None,
        help="Space-separated list of file extensions to include (e.g., .py .md).",
    )
    parser.add_argument(
        "--critical-keywords",
        nargs="*",
        default=None,
        help="Space-separated list of keywords to flag files as critical.",
    )

    args = parser.parse_args()

    # Normalize extensions to include leading dot if missing
    if args.extensions:
        args.extensions = [ext if ext.startswith('.') else '.' + ext for ext in args.extensions]
        args.extensions = [ext.lower() for ext in args.extensions] # Ensure consistent casing

    try:
        report = audit_directory(
            args.directory_path, args.extensions, args.critical_keywords
        )
        print(report)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
