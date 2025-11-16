import os
import sys

# Define survival scores for different file types
# Higher score means higher perceived importance in a post-apocalyptic scenario
SURVIVAL_SCORES = {
    '.md': 10,  # Documentation, crucial knowledge
    '.py': 8,   # Code, tools for rebuilding
    '.sh': 7,   # Scripts, automation
    '.json': 6, # Data, configuration
    '.yml': 6,  # Data, configuration
    '.txt': 5,  # Notes, raw information
    '.csv': 4,  # Tabular data
    '.log': 1,  # Ephemeral logs, less critical
    '': 0       # Files without extension
}

PRIORITY_LABELS = {
    10: 'High', 8: 'Medium', 7: 'Medium', 6: 'Medium', 5: 'Low', 4: 'Low', 1: 'Very Low', 0: 'Unknown'
}

def get_file_extension(filename):
    """Extracts the file extension, handling dotfiles and no-extension files."""
    parts = filename.split('.')
    if len(parts) > 1 and parts[-1]: # Has an extension
        return '.' + parts[-1].lower()
    elif len(parts) == 1: # No extension
        return ''
    else: # Dotfile like .gitignore
        return '.' + parts[-1].lower() if parts[-1] else ''

def audit_directory(path):
    """Recursively audits a directory, collecting file stats and survival scores."""
    if not os.path.isdir(path):
        raise ValueError(f"Error: Directory not found at '{path}'")

    total_files = 0
    total_size = 0
    file_type_stats = {}

    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                size = os.path.getsize(file_path)
                ext = get_file_extension(filename)

                total_files += 1
                total_size += size

                if ext not in file_type_stats:
                    file_type_stats[ext] = {'count': 0, 'size': 0, 'score': 0}

                file_type_stats[ext]['count'] += 1
                file_type_stats[ext]['size'] += size
                file_type_stats[ext]['score'] += SURVIVAL_SCORES.get(ext, 0)
            except OSError:
                # Silently skip unreadable files for audit
                pass

    return total_files, total_size, file_type_stats

def format_size(size_bytes):
    """Formats bytes into a human-readable string (KB, MB, GB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def generate_report(directory_path, total_files, total_size, file_type_stats):
    """Generates a formatted audit report."""
    report = []
    report.append(f"ApocalypsAI Digital Asset Audit Report for: {directory_path}")
    report.append("-" * (len(report[0])))
    report.append("")

    overall_readiness_score = sum(stats['score'] for stats in file_type_stats.values())

    report.append(f"Total Files Found: {total_files}")
    report.append(f"Total Size: {format_size(total_size)}")
    report.append(f"Overall Apocalypse Readiness Score: {overall_readiness_score}")
    report.append("")
    report.append("File Type Breakdown:")
    report.append("--------------------")

    # Sort by accumulated score descending, then by extension ascending for tie-breaking
    sorted_stats = sorted(
        file_type_stats.items(),
        key=lambda item: (-item[1]['score'], item[0])
    )

    for ext, stats in sorted_stats:
        # Get the base score for the extension, not the accumulated score, for priority label
        base_score = SURVIVAL_SCORES.get(ext, 0)
        priority_label = PRIORITY_LABELS.get(base_score, 'Unknown')
        report.append(
            f"{ext:<5}: {stats['count']} files, {format_size(stats['size']):>7}, Score: {stats['score']:<3} (Survival Priority: {priority_label})")

    return "\n".join(report)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 auditor.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    try:
        total_files, total_size, file_type_stats = audit_directory(directory_path)
        report = generate_report(directory_path, total_files, total_size, file_type_stats)
        print(report)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
