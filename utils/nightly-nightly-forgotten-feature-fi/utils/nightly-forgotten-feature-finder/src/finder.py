import os
import re
import sys

def find_forgotten_features(root_dir="."):
    """
    Scans files in the given root directory for common technical debt markers.
    Reports file path, line number, and the comment content.
    """
    markers = ["TODO", "FIXME", "HACK", "BUG", "XXX"]
    # Regex to find markers, case-insensitive, ensuring it's not part of a larger word.
    # It captures the marker and the rest of the line.
    marker_pattern = re.compile(r".*?(?<!\w)(?P<marker>" + "|".join(markers) + r")(?P<content>.*)", re.IGNORECASE)

    report = []
    
    # Common code file extensions to scan
    scannable_extensions = (
        '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.c', '.cpp', '.h', '.hpp',
        '.go', '.rs', '.php', '.rb', '.swift', '.kt', '.m', '.mm', '.sh', '.bash',
        '.zsh', '.ps1', '.bat', '.yml', '.yaml', '.json', '.xml', '.html', '.css',
        '.scss', '.less', '.md', '.txt', '.rst', '.toml', '.ini', '.cfg', '.env'
    )

    # Exclude common directories that usually don't contain relevant markers
    excluded_dirs = {
        '.git', '.svn', '.hg', '__pycache__', 'node_modules', 'venv', '.venv',
        'env', '.env', 'build', 'dist', 'target', '.idea', '.vscode', '.github'
    }

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to exclude directories from further traversal
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]

        for filename in filenames:
            if filename.lower().endswith(scannable_extensions):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            match = marker_pattern.search(line)
                            if match:
                                marker = match.group('marker').upper() # Normalize marker case
                                content = match.group('content').strip()
                                report.append(f"{filepath}:{line_num}: {marker}:{content}")
                except Exception as e:
                    # Silently skip unreadable files for robustness
                    pass 

    return report

def main():
    path_to_scan = sys.argv[1] if len(sys.argv) > 1 else "."
    
    print("Forgotten Features Report:\n")
    report = find_forgotten_features(path_to_scan)
    
    if report:
        for item in report:
            print(item)
    else:
        print("No forgotten features found. Your codebase is pristine!")

if __name__ == "__main__":
    main()
