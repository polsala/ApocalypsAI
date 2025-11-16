import os
import argparse
import datetime
import sys

def get_file_info(path):
    """Returns (size, mtime) for a given file path."""
    try:
        stat_info = os.stat(path)
        return stat_info.st_size, stat_info.st_mtime
    except OSError:
        return None, None

def format_bytes(size):
    """Formats bytes into a human-readable string (e.g., 1.2 GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"

def format_timedelta(timestamp):
    """Formats a timestamp into a human-readable age (e.g., 2 years, 3 months ago)."""
    now = datetime.datetime.now()
    file_dt = datetime.datetime.fromtimestamp(timestamp)
    delta = now - file_dt

    if delta.days < 0: # Future file, unlikely but handle
        return "in the future"
    elif delta.days < 1:
        return "today"
    elif delta.days < 30:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.days < 365:
        months = delta.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = delta.days // 365
        remaining_days = delta.days % 365
        months = remaining_days // 30
        parts = []
        if years > 0:
            parts.append(f"{years} year{'s' if years > 1 else ''}")
        if months > 0:
            parts.append(f"{months} month{'s' if months > 1 else ''}")
        return f"{', '.join(parts)} ago" if parts else f"{delta.days} days ago"


def generate_report(paths, min_size_mb, min_age_days, top_n):
    """
    Scans specified paths and generates a Markdown report of disk usage,
    largest files, and oldest files.
    """
    all_files = []
    total_scanned_size = 0
    total_files_scanned = 0
    total_dirs_scanned = 0
    now_timestamp = datetime.datetime.now().timestamp()
    min_age_timestamp = now_timestamp - (min_age_days * 24 * 60 * 60)
    min_size_bytes = min_size_mb * 1024 * 1024

    for path_root in paths:
        if not os.path.exists(path_root):
            print(f"Warning: Path not found - {path_root}", file=sys.stderr)
            continue
        if not os.path.isdir(path_root):
            print(f"Warning: Path is not a directory - {path_root}", file=sys.stderr)
            continue

        for root, dirs, files in os.walk(path_root):
            total_dirs_scanned += 1
            for file_name in files:
                file_path = os.path.join(root, file_name)
                size, mtime = get_file_info(file_path)
                if size is not None and mtime is not None:
                    total_scanned_size += size
                    total_files_scanned += 1
                    all_files.append({'path': file_path, 'size': size, 'mtime': mtime})

    # Sort for largest files
    largest_files = sorted([f for f in all_files if f['size'] >= min_size_bytes],
                           key=lambda x: x['size'], reverse=True)[:top_n]

    # Sort for oldest files
    oldest_files = sorted([f for f in all_files if f['mtime'] <= min_age_timestamp],
                          key=lambda x: x['mtime'])[:top_n]

    report_lines = []
    report_lines.append(f"# Rubble Report for {', '.join(paths)}")
    report_lines.append(f"\n**Generated On:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    report_lines.append("## Scan Summary")
    report_lines.append(f"*   **Total Scanned Size:** {format_bytes(total_scanned_size)}")
    report_lines.append(f"*   **Total Files Scanned:** {total_files_scanned}")
    report_lines.append(f"*   **Total Directories Scanned:** {total_dirs_scanned}\n")

    report_lines.append(f"## Top {top_n} Largest Files (>= {min_size_mb} MB)")
    if largest_files:
        for i, file_info in enumerate(largest_files):
            report_lines.append(f"{i+1}. `{format_bytes(file_info['size'])}` - `{file_info['path']}`")
    else:
        report_lines.append("No large files found matching criteria.")
    report_lines.append("")

    report_lines.append(f"## Top {top_n} Oldest Files (>= {min_age_days} days)")
    if oldest_files:
        for i, file_info in enumerate(oldest_files):
            report_lines.append(f"{i+1}. `{format_timedelta(file_info['mtime'])}` - `{file_info['path']}`")
    else:
        report_lines.append("No old files found matching criteria.")
    report_lines.append("\n---\n*End of Report*")

    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a Rubble Report of disk usage, largest, and oldest files."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="One or more directories to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--min-size",
        type=int,
        default=50,
        help="Minimum size in MB for a file to be considered 'large'. Default: 50 MB."
    )
    parser.add_argument(
        "--min-age",
        type=int,
        default=180,
        help="Minimum age in days for a file to be considered 'old'. Default: 180 days."
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=10,
        help="Number of top largest/oldest files to list. Default: 10."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output filename for the Markdown report. If not provided, prints to stdout."
    )

    args = parser.parse_args()

    report_content = generate_report(args.path, args.min_size, args.min_age, args.top_n)

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"Rubble Report saved to {args.output}")
        except IOError as e:
            print(f"Error writing report to file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report_content)

if __name__ == "__main__":
    main()
