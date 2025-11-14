import re
import sys
from collections import defaultdict

class CosmicDustCollector:
    """
    Scans log files for predefined error/warning patterns and categorizes them.
    """

    # Whimsical names for different anomaly types
    ANOMALY_TYPES = {
        "WARNING": "Cosmic Dust Bunnies",
        "ERROR": "Gravitational Glitches",
        "CRITICAL": "Temporal Anomalies",
        "EXCEPTION": "Temporal Anomalies",
    }

    # Regex patterns for detecting anomalies (case-insensitive)
    # Order matters for some overlaps, e.g., EXCEPTION is also an ERROR, but we want to catch it specifically.
    ANOMALY_PATTERNS = {
        "CRITICAL": re.compile(r".*(CRITICAL|FATAL|PANIC|UNHANDLED EXCEPTION).*"),
        "EXCEPTION": re.compile(r".*(EXCEPTION|TRACEBACK|STACKTRACE).*"),
        "ERROR": re.compile(r".*(ERROR|FAILED|FAILURE|DENIED|UNAUTHORIZED|REFUSED|TIMEOUT).*"),
        "WARNING": re.compile(r".*(WARN|WARNING|DEPRECATED|UNEXPECTED|SLOW).*"),
    }

    def __init__(self):
        self.results = defaultdict(lambda: defaultdict(list)) # {filepath: {anomaly_type: [lines]}}
        self.total_counts = defaultdict(int) # {anomaly_type: count}

    def _categorize_line(self, line: str) -> str | None:
        """
        Categorizes a single log line based on predefined patterns.
        Returns the anomaly type (e.g., "ERROR") or None if no match.
        """
        for anomaly_type, pattern in self.ANOMALY_PATTERNS.items():
            if pattern.search(line.upper()): # Convert to upper for case-insensitive matching
                return anomaly_type
        return None

    def collect_dust(self, filepath: str):
        """
        Scans a single log file for anomalies and stores the results.
        """
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    anomaly_raw_type = self._categorize_line(line.strip())
                    if anomaly_raw_type:
                        whimsical_type = self.ANOMALY_TYPES.get(anomaly_raw_type, anomaly_raw_type)
                        self.results[filepath][whimsical_type].append(line.strip())
                        self.total_counts[whimsical_type] += 1
        except FileNotFoundError:
            self.results[filepath][self.ANOMALY_TYPES["ERROR"]].append(f"File not found: {filepath}")
            self.total_counts[self.ANOMALY_TYPES["ERROR"]] += 1 # Count file not found as an error
        except Exception as e:
            self.results[filepath][self.ANOMALY_TYPES["ERROR"]].append(f"Error processing {filepath}: {e}")
            self.total_counts[self.ANOMALY_TYPES["ERROR"]] += 1

    def generate_report(self) -> str:
        """
        Generates a formatted report of all collected anomalies.
        """
        report_parts = ["🌌 Cosmic Dust Collector Report 🌌\n"]

        for filepath, anomalies in self.results.items():
            report_parts.append(f"Scanning: {filepath}")
            report_parts.append("-" * 50)

            # Ensure consistent order for reporting
            for raw_type in ["WARNING", "ERROR", "CRITICAL", "EXCEPTION"]:
                whimsical_type = self.ANOMALY_TYPES.get(raw_type, raw_type)
                lines = anomalies.get(whimsical_type, [])
                report_parts.append(f"{self._get_emoji(whimsical_type)} {whimsical_type} ({self._get_short_name(whimsical_type)}): {len(lines)}")
                if lines:
                    for line in lines[:2]: # Show up to 2 example lines
                        report_parts.append(f"  - {line}")
                else:
                    report_parts.append(f"  - No {self._get_short_name(whimsical_type).lower()} detected.")
            report_parts.append("\n")

        report_parts.append("---\nSummary for all files:")
        for raw_type in ["WARNING", "ERROR", "CRITICAL", "EXCEPTION"]:
            whimsical_type = self.ANOMALY_TYPES.get(raw_type, raw_type)
            count = self.total_counts.get(whimsical_type, 0)
            report_parts.append(f"Total {whimsical_type}: {count}")

        return "\n".join(report_parts)

    def _get_emoji(self, whimsical_type: str) -> str:
        """Returns an emoji for a given whimsical type."""
        if "Dust Bunnies" in whimsical_type:
            return "✨"
        elif "Glitches" in whimsical_type:
            return "💥"
        elif "Anomalies" in whimsical_type:
            return "⏳"
        return "❓"

    def _get_short_name(self, whimsical_type: str) -> str:
        """Returns a short name for a given whimsical type."""
        if "Dust Bunnies" in whimsical_type:
            return "warnings"
        elif "Glitches" in whimsical_type:
            return "errors"
        elif "Anomalies" in whimsical_type:
            return "exceptions/criticals"
        return "anomalies"


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/dust_collector.py <path_to_log_file_1> [path_to_log_file_2 ...]")
        sys.exit(1)

    collector = CosmicDustCollector()
    for filepath in sys.argv[1:]:
        collector.collect_dust(filepath)

    print(collector.generate_report())

if __name__ == "__main__":
    main()
