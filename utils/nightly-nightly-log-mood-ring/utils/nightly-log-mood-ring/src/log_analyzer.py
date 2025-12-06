import os
import argparse
from datetime import datetime
from collections import defaultdict

class LogMoodAnalyzer:
    """
    Analyzes log files for sentiment keywords and determines an overall "mood".
    """

    MOOD_KEYWORDS = {
        "CRITICAL": -5,
        "ERROR": -3,
        "WARNING": -1,
        "SUCCESS": 2,
        "INFO": 0,
    }

    MOOD_EMOJIS = {
        "💀": "Catastrophic", # Score < -10
        "🚨": "Alarming",     # Score < -5
        "😬": "Anxious",      # Score < 0
        "💬": "Neutral",      # Score == 0
        "✨": "Optimistic",   # Score > 0 and < 5
        "✅": "Serene",       # Score >= 5
    }

    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self.total_counts = defaultdict(int)

    def _get_mood_from_score(self, score: int) -> tuple[str, str]:
        """Determines the emoji and description based on a mood score."""
        if score <= -10:
            return "💀", self.MOOD_EMOJIS["💀"]
        elif score <= -5:
            return "🚨", self.MOOD_EMOJIS["🚨"]
        elif score < 0:
            return "😬", self.MOOD_EMOJIS["😬"]
        elif score == 0:
            return "💬", self.MOOD_EMOJIS["💬"]
        elif score > 0 and score < 5:
            return "✨", self.MOOD_EMOJIS["✨"]
        else: # score >= 5
            return "✅", self.MOOD_EMOJIS["✅"]

    def analyze_log_file(self, filepath: str) -> dict:
        """
        Analyzes a single log file for keyword occurrences and calculates its mood.
        Returns a dictionary with counts, score, emoji, and description.
        """
        counts = defaultdict(int)
        mood_score = 0

        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    for keyword, weight in self.MOOD_KEYWORDS.items():
                        if keyword in line.upper():
                            counts[keyword] += 1
                            mood_score += weight
        except IOError as e:
            print(f"Warning: Could not read file {filepath}: {e}")
            return {"counts": counts, "score": 0, "emoji": "❓", "description": "Unreadable"}

        emoji, description = self._get_mood_from_score(mood_score)
        return {"counts": counts, "score": mood_score, "emoji": emoji, "description": description}

    def scan_and_analyze(self) -> dict:
        """
        Scans the specified directory for log files and performs analysis.
        Returns a dictionary containing per-file analysis and overall system mood.
        """
        results = {}
        log_files_found = []

        for root, _, files in os.walk(self.log_dir):
            for file in files:
                if file.endswith(".log"):
                    log_files_found.append(os.path.join(root, file))

        if not log_files_found:
            return {"files": {}, "overall_mood": {"emoji": "🤷", "description": "No logs found", "counts": self.total_counts}}

        for filepath in sorted(log_files_found): # Sort for deterministic output
            file_analysis = self.analyze_log_file(filepath)
            results[filepath] = file_analysis
            for keyword, count in file_analysis["counts"].items():
                self.total_counts[keyword] += count

        overall_score = sum(self.total_counts[k] * self.MOOD_KEYWORDS[k] for k in self.total_counts)
        overall_emoji, overall_description = self._get_mood_from_score(overall_score)

        return {
            "files": results,
            "overall_mood": {
                "emoji": overall_emoji,
                "description": overall_description,
                "counts": self.total_counts
            }
        }

    def print_report(self, analysis_results: dict):
        """Prints a formatted report of the analysis results."""
        print(f"Nightly Log Mood Ring Report ({datetime.now().strftime('%Y-%m-%d')})\n")
        print(f"Scanning logs in: {self.log_dir}\n")

        if not analysis_results["files"]:
            print(f"Overall System Mood: {analysis_results['overall_mood']['emoji']} ({analysis_results['overall_mood']['description']})")
            print("No .log files found to analyze.")
            return

        for filepath, data in analysis_results["files"].items():
            print(f"--- {os.path.basename(filepath)} ---")
            print(f"Mood: {data['emoji']} ({data['description']})")
            for keyword in sorted(self.MOOD_KEYWORDS.keys()): # Sort for deterministic output
                print(f"  {keyword}: {data['counts'][keyword]}")
            print()

        print("--- Overall System Mood ---")
        overall_mood = analysis_results["overall_mood"]
        print(f"Mood: {overall_mood['emoji']} ({overall_mood['description']})")
        for keyword in sorted(self.MOOD_KEYWORDS.keys()): # Sort for deterministic output
            print(f"  Total {keyword}: {overall_mood['counts'][keyword]}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Log Mood Ring: Analyze log files for sentiment."
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Directory to scan for .log files (default: current directory)."
    )
    args = parser.parse_args()

    analyzer = LogMoodAnalyzer(args.path)
    results = analyzer.scan_and_analyze()
    analyzer.print_report(results)

if __name__ == "__main__":
    main()
