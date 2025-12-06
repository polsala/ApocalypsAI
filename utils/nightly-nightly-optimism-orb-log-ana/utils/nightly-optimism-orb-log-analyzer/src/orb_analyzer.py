import os
import argparse
from collections import defaultdict

class OptimismOrbAnalyzer:
    """
    Scans log files for positive keywords and generates an optimism report.
    """
    def __init__(self, keywords=None):
        self.positive_keywords = {
            "success", "completed", "deployed", "resolved", "achieved",
            "victory", "progress", "fixed", "online", "healthy", "optimistic"
        }
        if keywords:
            self.positive_keywords.update(set(k.lower() for k in keywords))

    def _read_file_content(self, filepath):
        """Reads the content of a file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Warning: Could not read file {filepath}: {e}")
            return ""

    def analyze_directory(self, log_directory):
        """
        Analyzes all log files in a given directory for positive keywords.
        Returns a dictionary of keyword counts and a list of files processed.
        """
        if not os.path.isdir(log_directory):
            raise ValueError(f"Directory not found: {log_directory}")

        keyword_counts = defaultdict(int)
        processed_files = []

        for root, _, files in os.walk(log_directory):
            for filename in files:
                if filename.lower().endswith(('.log', '.txt')):
                    filepath = os.path.join(root, filename)
                    content = self._read_file_content(filepath)
                    if content:
                        processed_files.append(filepath)
                        for keyword in self.positive_keywords:
                            keyword_counts[keyword] += content.lower().count(keyword)
        return dict(keyword_counts), processed_files

    def generate_report(self, keyword_counts, processed_files):
        """
        Generates a Markdown-formatted report from the analysis results.
        """
        total_positives = sum(keyword_counts.values())
        report_lines = [
            "# 🌟 Nightly Optimism Orb Report 🌟",
            "",
            "Greetings, fellow cosmic travelers! The Optimism Orb has spun its magic,",
            "sifting through the digital ether to bring you a beacon of positivity.",
            "",
            f"## ✨ Summary of Digital Sunshine ✨",
            f"**Total Positive Mentions Found:** `{total_positives}` across `{len(processed_files)}` files.",
            "",
            "The universe whispers its successes through these keywords:",
            ""
        ]

        if not keyword_counts:
            report_lines.append("No positive keywords detected in the scanned logs. Keep shining!")
        else:
            sorted_counts = sorted(keyword_counts.items(), key=lambda item: item[1], reverse=True)
            for keyword, count in sorted_counts:
                if count > 0:
                    report_lines.append(f"- `{keyword}`: `{count}` times")

        if processed_files:
            report_lines.append("\n## 📜 Files Scanned 📜")
            for f in processed_files:
                report_lines.append(f"- `{f}`")
        else:
            report_lines.append("\nNo log files were found or processed in the specified directory.")

        report_lines.append("\n---")
        report_lines.append("May your systems be stable and your spirits high!")
        return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Optimism Orb Log Analyzer: Scans log files for positive keywords."
    )
    parser.add_argument(
        "log_directory",
        help="The directory containing log files to scan."
    )
    parser.add_argument(
        "--keywords",
        nargs='*',
        help="Additional positive keywords to search for (space-separated)."
    )
    args = parser.parse_args()

    try:
        analyzer = OptimismOrbAnalyzer(keywords=args.keywords)
        keyword_counts, processed_files = analyzer.analyze_directory(args.log_directory)
        report = analyzer.generate_report(keyword_counts, processed_files)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
