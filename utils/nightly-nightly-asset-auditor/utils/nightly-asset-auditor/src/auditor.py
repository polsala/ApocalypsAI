import os
import sys
from collections import defaultdict

def get_survival_score(extension):
    """Assigns a survival score based on file extension."""
    critical_extensions = {'.md', '.txt', '.json', '.yaml', '.yml', '.toml'}
    essential_extensions = {'.py', '.sh', '.js', '.ts', '.go', '.rs', '.java', '.c', '.cpp', '.h'}
    useful_extensions = {'.log', '.csv', '.xml', '.html', '.css'}
    junk_extensions = {'.tmp', '.bak', '.old', '.zip', '.tar.gz', '.DS_Store', '.gitkeep', '.gitignore'}

    if extension in critical_extensions:
        return 5, "Critical"
    elif extension in essential_extensions:
        return 3, "Essential"
    elif extension in useful_extensions:
        return 1, "Useful"
    elif extension in junk_extensions:
        return 0, "Junk"
    else:
        return 0, "Unknown"

def get_extension_description(extension):
    """Provides a human-readable description for common extensions."""
    descriptions = {
        '.py': 'Python Source',
        '.md': 'Markdown Document',
        '.txt': 'Plain Text',
        '.json': 'JSON Data',
        '.yaml': 'YAML Configuration',
        '.yml': 'YAML Configuration',
        '.toml': 'TOML Configuration',
        '.sh': 'Shell Script',
        '.js': 'JavaScript Source',
        '.ts': 'TypeScript Source',
        '.go': 'Go Source',
        '.rs': 'Rust Source',
        '.java': 'Java Source',
        '.c': 'C Source',
        '.cpp': 'C++ Source',
        '.h': 'Header File',
        '.log': 'Log File',
        '.csv': 'Comma Separated Values',
        '.xml': 'XML Data',
        '.html': 'HTML Document',
        '.css': 'CSS Stylesheet',
        '.tmp': 'Temporary File',
        '.bak': 'Backup File',
        '.old': 'Old Version File',
        '.zip': 'ZIP Archive',
        '.tar.gz': 'Compressed Archive',
        '.DS_Store': 'macOS System File',
        '.gitkeep': 'Git Placeholder',
        '.gitignore': 'Git Ignore Rules',
    }
    return descriptions.get(extension, f"'{extension}' File")

def audit_directory(path):
    """
    Scans a directory and its subdirectories, categorizing files,
    calculating sizes, and assigning survival scores.
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directory not found: {path}")

    file_stats = defaultdict(lambda: {'count': 0, 'size': 0, 'score': 0, 'score_type': 'Unknown'})
    total_files = 0
    total_size = 0
    overall_survival_score = 0

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                _, ext = os.path.splitext(file)
                ext = ext.lower() # Normalize extension

                score, score_type = get_survival_score(ext)

                file_stats[ext]['count'] += 1
                file_stats[ext]['size'] += size
                file_stats[ext]['score'] += score
                file_stats[ext]['score_type'] = score_type # This will be overwritten, but it's fine as score_type is per-extension

                total_files += 1
                total_size += size
                overall_survival_score += score
            except OSError as e:
                print(f"Warning: Could not access file {file_path} - {e}", file=sys.stderr)
                continue

    return {
        'target_path': path,
        'total_files': total_files,
        'total_size': total_size,
        'overall_survival_score': overall_survival_score,
        'file_type_breakdown': dict(file_stats)
    }

def format_size(size_bytes):
    """Formats bytes into human-readable string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def print_report(audit_results):
    """Prints the audit results in a human-readable format."""
    print(f"ApocalypsAI Asset Audit Report for: {audit_results['target_path']}\n")
    print("--- Overall Summary ---")
    print(f"Total Files Scanned: {audit_results['total_files']}")
    print(f"Total Size: {format_size(audit_results['total_size'])}")
    print(f"Overall Survival Score: {audit_results['overall_survival_score']} points\n")

    print("--- File Type Breakdown ---")
    # Sort by score_type (Critical, Essential, Useful, Junk, Unknown) then by extension
    score_type_order = {"Critical": 0, "Essential": 1, "Useful": 2, "Junk": 3, "Unknown": 4}
    sorted_breakdown = sorted(
        audit_results['file_type_breakdown'].items(),
        key=lambda item: (score_type_order[item[1]['score_type']], item[0])
    )

    for ext, stats in sorted_breakdown:
        description = get_extension_description(ext)
        print(f"{ext} ({description})")
        print(f"  Files: {stats['count']}")
        print(f"  Size: {format_size(stats['size'])}")
        print(f"  Survival Score: {stats['score']} ({stats['score_type']})\n")

    print("--- Survival Score Legend ---")
    print("*   **Critical (5 points/file)**: Documentation, Configuration, Core Data")
    print("*   **Essential (3 points/file)**: Source Code, Key Scripts")
    print("*   **Useful (1 point/file)**: Logs, Auxiliary Data, Web Assets")
    print("*   **Junk (0 points/file)**: Temporary, Backups, Archives, System Files")
    print("*   **Unknown (0 points/file)**: Uncategorized files")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/auditor.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    try:
        results = audit_directory(target_directory)
        print_report(results)
        sys.exit(0)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
