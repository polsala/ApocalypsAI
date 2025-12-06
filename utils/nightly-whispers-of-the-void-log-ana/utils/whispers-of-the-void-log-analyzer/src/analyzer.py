import re
import os
from collections import Counter

class LogAnalyzer:
    def __init__(self, whisper_patterns=None, anomaly_threshold=3):
        """
        Initializes the LogAnalyzer.

        Args:
            whisper_patterns (list): A list of regex patterns to look for.
                                     If None, uses a default set of common error/warning patterns.
            anomaly_threshold (int): The minimum number of occurrences for a pattern
                                     to be considered an "anomaly" or "whisper".
        """
        self.whisper_patterns = whisper_patterns if whisper_patterns is not None else self._default_patterns()
        self.anomaly_threshold = anomaly_threshold

    def _default_patterns(self):
        """Provides a default set of common log patterns indicating potential issues."""
        return [
            r"error",
            r"fail",
            r"exception",
            r"timeout",
            r"denied",
            r"resource limit",
            r"memory exhausted",
            r"disk full",
            r"unhandled",
            r"deprecated",
            r"warning",
            r"critical",
        ]

    def analyze_log_file(self, file_path):
        """
        Analyzes a log file for predefined "whisper" patterns.

        Args:
            file_path (str): The path to the log file.

        Returns:
            dict: A dictionary containing detected anomalies, their counts,
                  and a summary message.
        """
        if not os.path.exists(file_path):
            return {
                "anomalies": {},
                "summary": f"Error: File not found at {file_path}",
                "status": "error"
            }

        pattern_counts = Counter()
        total_lines = 0
        detected_anomalies = {}

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    total_lines += 1
                    for pattern_str in self.whisper_patterns:
                        if re.search(pattern_str, line, re.IGNORECASE):
                            pattern_counts[pattern_str] += 1
        except Exception as e:
            return {
                "anomalies": {},
                "summary": f"Error reading file {file_path}: {e}",
                "status": "error"
            }

        for pattern, count in pattern_counts.items():
            if count >= self.anomaly_threshold:
                detected_anomalies[pattern] = count

        if detected_anomalies:
            summary = f"Detected {len(detected_anomalies)} potential 'whispers of the void' in {total_lines} lines."
            status = "anomalies_detected"
        elif total_lines == 0:
            summary = "The log file is empty. No whispers detected."
            status = "empty_log"
        else:
            summary = f"No significant 'whispers of the void' detected above threshold in {total_lines} lines."
            status = "clean"

        return {
            "anomalies": detected_anomalies,
            "total_lines": total_lines,
            "summary": summary,
            "status": status
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Whispers of the Void Log Analyzer: Scans log files for subtle patterns indicating potential issues."
    )
    parser.add_argument("log_file", help="Path to the log file to analyze.")
    parser.add_argument("--threshold", type=int, default=3,
                        help="Minimum occurrences for a pattern to be considered an anomaly (default: 3).")
    parser.add_argument("--patterns", nargs='*',
                        help="Space-separated list of custom regex patterns to search for. "
                             "Overrides default patterns if provided.")

    args = parser.parse_args()

    analyzer = LogAnalyzer(whisper_patterns=args.patterns, anomaly_threshold=args.threshold)
    result = analyzer.analyze_log_file(args.log_file)

    print(f"--- Analysis of '{args.log_file}' ---")
    print(f"Status: {result['status'].replace('_', ' ').title()}")
    print(f"Summary: {result['summary']}")
    if result['anomalies']:
        print("\nDetected Whispers (Pattern: Count):")
        for pattern, count in result['anomalies'].items():
            print(f"- '{pattern}': {count}")
    print("-----------------------------------")

if __name__ == "__main__":
    main()
