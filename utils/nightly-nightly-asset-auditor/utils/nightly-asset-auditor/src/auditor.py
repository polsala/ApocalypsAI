import os
import sys
from datetime import datetime

# Define survival scores for different file extensions
# Higher score means more critical for 'survival'
SURVIVAL_SCORES = {
    # Critical (5)
    '.py': 5, '.sh': 5, '.yml': 5, '.yaml': 5, '.json': 5, '.js': 5, '.ts': 5,
    '.go': 5, '.rs': 5, '.java': 5, '.c': 5, '.cpp': 5, '.h': 5, '.hpp': 5,
    '.md': 5, '.toml': 5, '.ini': 5, '.env': 5, '.sql': 5,

    # Useful (3)
    '.txt': 3, '.csv': 3, '.xml': 3, '.log': 3, '.html': 3, '.css': 3,
    '.pdf': 3, '.doc': 3, '.docx': 3, '.xls': 3, '.xlsx': 3, '.ppt': 3, '.pptx': 3,

    # Disposable (1)
    '.tmp': 1, '.bak': 1, '.zip': 1, '.tar.gz': 1, '.rar': 1, '.7z': 1,
    '.DS_Store': 1, '.gitkeep': 1, '.swp': 1, '.pyc': 1, '.o': 1, '.so': 1, '.dll': 1,

    # Default for unknown types
    '': 0 # Files without extension or unknown
}

class AssetAuditor:
    def __init__(self, base_path: str):
        if not os.path.isdir(base_path):
            raise ValueError(f"Error: Directory not found at '{base_path}'")
        self.base_path = base_path
        self.file_stats = {}
        self.total_files = 0
        self.total_size = 0

    def _get_survival_score(self, extension: str) -> int:
        """Returns the survival score for a given file extension."""
        return SURVIVAL_SCORES.get(extension.lower(), SURVIVAL_SCORES[''])

    def audit(self):
        """Performs the directory audit and collects file statistics."""
        for root, _, files in os.walk(self.base_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if not os.path.isfile(file_path): # Skip if it's not a regular file (e.g., broken symlink)
                    continue

                try:
                    size = os.path.getsize(file_path)
                    _, ext = os.path.splitext(file_name)
                    ext = ext.lower()

                    if ext not in self.file_stats:
                        self.file_stats[ext] = {'count': 0, 'size': 0, 'score': self._get_survival_score(ext)}

                    self.file_stats[ext]['count'] += 1
                    self.file_stats[ext]['size'] += size
                    self.total_files += 1
                    self.total_size += size
                except OSError as e:
                    # Handle cases where file might be inaccessible or disappear during walk
                    print(f"Warning: Could not access file '{file_path}': {e}", file=sys.stderr)
                    continue

    def _format_size(self, size_bytes: int) -> str:
        """Formats bytes into a human-readable string (KB, MB, GB)."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes / (1024**2):.1f} MB"
        else:
            return f"{size_bytes / (1024**3):.1f} GB"

    def generate_report(self) -> str:
        """Generates a Markdown formatted report of the audit findings."""
        report_lines = []
        report_lines.append(f"# Digital Asset Audit Report: {self.base_path}")
        report_lines.append(f"\n## Audit Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        report_lines.append("| File Type | Count | Total Size | Survival Score | Notes |")
        report_lines.append("| :-------- | :---- | :--------- | :------------- | :---- |")

        # Sort by survival score (descending) then by file type
        sorted_stats = sorted(
            self.file_stats.items(),
            key=lambda item: (item[1]['score'], item[0]),
            reverse=True
        )

        score_notes = {
            5: 'Critical', 3: 'Useful', 1: 'Disposable', 0: 'Irrelevant'
        }

        for ext, stats in sorted_stats:
            ext_display = ext if ext else '(No Extension)'
            score_text = f"{stats['score']} ({score_notes.get(stats['score'], 'Unknown')})"
            report_lines.append(
                f"| {ext_display} | {stats['count']} | {self._format_size(stats['size'])} | {score_text} | |")

        report_lines.append("\n## Summary\n")
        report_lines.append(f"Total Files Scanned: {self.total_files}")
        report_lines.append(f"Total Size Scanned: {self._format_size(self.total_size)}")
        report_lines.append("\n*Prioritize files with higher survival scores for backup and preservation.*")

        return "\n".join(report_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 auditor.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]
    try:
        auditor = AssetAuditor(target_directory)
        auditor.audit()
        print(auditor.generate_report())
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
