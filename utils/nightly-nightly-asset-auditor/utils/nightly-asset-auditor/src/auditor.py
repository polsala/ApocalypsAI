import os
import sys
from collections import defaultdict

# Define survival score categories and their associated extensions
SURVIVAL_SCORES = {
    'Critical': ['.md', '.txt', '.json', '.yaml', '.yml', '.csv'],
    'Important': ['.py', '.sh', '.js', '.go', '.rs', '.java', '.cpp', '.h'],
    'Useful': ['.log', '.xml', '.html', '.css', '.pdf', '.zip', '.tar.gz'],
    'Ephemeral': ['.tmp', '.bak', '.swp', '.DS_Store'],
}

def get_survival_category(extension):
    """Determines the survival category for a given file extension."""
    for category, extensions in SURVIVAL_SCORES.items():
        if extension in extensions:
            return category
    return 'Unknown'

def audit_directory(root_dir):
    """Recursively audits a directory, categorizing files and calculating sizes.

    Args:
        root_dir (str): The path to the directory to audit.

    Returns:
        dict: A dictionary containing audit results.
    """
    if not os.path.isdir(root_dir):
        raise ValueError(f"Directory not found: {root_dir}")

    results = defaultdict(lambda: {'count': 0, 'size': 0, 'category': 'Unknown'})
    total_files = 0
    total_size = 0

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(file_path)
                _, ext = os.path.splitext(filename)
                ext = ext.lower() # Normalize extension

                if not ext: # Handle files without extensions
                    ext = '[no_extension]'

                category = get_survival_category(ext)

                results[ext]['count'] += 1
                results[ext]['size'] += size
                results[ext]['category'] = category # Update category for the extension

                total_files += 1
                total_size += size
            except OSError: # Handle permission errors or broken symlinks
                # print(f"Warning: Could not access {file_path}", file=sys.stderr)
                pass # Skip inaccessible files

    return {
        'file_type_summary': dict(results),
        'total_files': total_files,
        'total_size': total_size,
        'root_dir': root_dir
    }

def format_size(size_bytes):
    """Formats a size in bytes to a human-readable string."""
    if size_bytes == 0: return "0 B"
    size_names = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def generate_report(audit_results):
    """Generates a Markdown report from audit results."""
    report = []
    report.append(f"# Asset Audit Report for '{audit_results['root_dir']}'\n")
    report.append(f"*Generated on: {os.path.getmtime(audit_results['root_dir']) if os.path.exists(audit_results['root_dir']) else 'N/A'}*\n") # Using mtime of root for a timestamp
    report.append(f"\n## Summary\n")
    report.append(f"- **Total Files Scanned**: {audit_results['total_files']}")
    report.append(f"- **Total Size**: {format_size(audit_results['total_size'])}\n")

    report.append("## File Type Breakdown\n")
    report.append("| Extension | Count | Total Size | Survival Score |\n")
    report.append("| :-------- | :---- | :--------- | :------------- |\n")

    # Sort by survival category then by count (descending)
    sorted_items = sorted(
        audit_results['file_type_summary'].items(),
        key=lambda item: (list(SURVIVAL_SCORES.keys()).index(item[1]['category']) if item[1]['category'] != 'Unknown' else len(SURVIVAL_SCORES)),
        reverse=False
    )

    for ext, data in sorted_items:
        report.append(
            f"| `{ext}` | {data['count']} | {format_size(data['size'])} | {data['category']} |\n"
        )

    return "".join(report)

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/auditor.py <path_to_directory>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]

    try:
        results = audit_directory(target_directory)
        report = generate_report(results)
        print(report)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
