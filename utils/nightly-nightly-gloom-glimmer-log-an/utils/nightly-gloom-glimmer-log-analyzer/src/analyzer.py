import sys
import re
from collections import defaultdict

class LogAnalyzer:
    def __init__(self):
        # Patterns for 'Gloom' (negative) events. Order matters for categorization priority.
        self.gloom_patterns = {
            "ERROR": re.compile(r".*(ERROR|FAILURE|FAILED|CRITICAL|DENIED|UNAUTHORIZED|EXCEPTION|TIMEOUT).*"),
            "WARNING": re.compile(r".*(WARNING|ALERT|LOW POWER|DISK FULL|MEMORY LEAK|DEGRADED).*"),
        }
        # Patterns for 'Glimmer' (positive) events. Order matters for categorization priority.
        self.glimmer_patterns = {
            "SUCCESS": re.compile(r".*(SUCCESS|COMPLETED|OK|READY|ONLINE|OPTIMIZED|HEALED|RESTORED|RECOVERED).*"),
            "INFO": re.compile(r".*(INFO|STARTUP|INITIATED|CONNECTED|ADJUSTED|STABLE|HEALTHY).*"),
        }
        self.gloom_counts = defaultdict(int)
        self.glimmer_counts = defaultdict(int)

    def analyze_log(self, log_file_path: str):
        """
        Analyzes a log file, categorizing lines into 'Gloom' or 'Glimmer'.
        A line is categorized as Gloom if any gloom pattern matches. If not gloom,
        it's then categorized as Glimmer if any glimmer pattern matches.
        """
        try:
            with open(log_file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    is_gloom = False
                    for category, pattern in self.gloom_patterns.items():
                        if pattern.search(line.upper()): # Convert to upper for case-insensitive matching
                            self.gloom_counts[category] += 1
                            is_gloom = True
                            break # Categorize as gloom and move to next line

                    if not is_gloom: # Only check for glimmer if not already categorized as gloom
                        for category, pattern in self.glimmer_patterns.items():
                            if pattern.search(line.upper()): # Convert to upper for case-insensitive matching
                                self.glimmer_counts[category] += 1
                                break # Categorize as glimmer and move to next line
        except FileNotFoundError:
            print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"An error occurred while reading the log file: {e}", file=sys.stderr)
            sys.exit(1)

    def generate_summary(self, log_file_path: str) -> str:
        """
        Generates a formatted summary of the analysis.
        """
        total_gloom = sum(self.gloom_counts.values())
        total_glimmer = sum(self.glimmer_counts.values())

        summary_output = [
            "--- Gloom-Glimmer Log Analysis ---",
            f"Log File: {log_file_path}",
            "",
            "Gloom (Negative Events):"
        ]

        if total_gloom == 0:
            summary_output.append("  No significant gloom detected. Keep up the good work!")
        else:
            for category, count in self.gloom_counts.items():
                summary_output.append(f"  - {category}: {count} occurrence(s)")
            summary_output.append(f"Total Gloom Events: {total_gloom}")

        summary_output.append("")
        summary_output.append("Glimmer (Positive Events):")

        if total_glimmer == 0:
            summary_output.append("  No significant glimmer detected. Stay vigilant!")
        else:
            for category, count in self.glimmer_counts.items():
                summary_output.append(f"  - {category}: {count} occurrence(s)")
            summary_output.append(f"Total Glimmer Events: {total_glimmer}")

        summary_output.append("")
        if total_glimmer > total_gloom:
            summary_output.append("Overall Morale: Optimistic! Glimmers outshine the Gloom.")
        elif total_gloom > total_glimmer:
            summary_output.append("Overall Morale: Cautious. Gloom is prevalent. Stay alert!")
        else:
            summary_output.append("Overall Morale: Balanced. A mix of highs and lows.")

        return "\n".join(summary_output)

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/analyzer.py <path_to_log_file>", file=sys.stderr)
        sys.exit(1)

    log_file_path = sys.argv[1]
    analyzer = LogAnalyzer()
    analyzer.analyze_log(log_file_path)
    print(analyzer.generate_summary(log_file_path))

if __name__ == "__main__":
    main()
