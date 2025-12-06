import re
import json
import sys
import argparse

class LogHarmonizer:
    """
    Transforms unstructured log lines into a consistent, machine-readable JSON format.
    """

    # Predefined patterns for common log formats.
    # Named capture groups will become JSON keys.
    # The order of patterns matters; more specific patterns should come first.
    PATTERNS = [
        {
            "name": "apache_access",
            "regex": r'^(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\d+)$'
        },
        {
            "name": "timestamped_message_with_user_ip",
            "regex": r'^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (?P<level>\w+): User \'(?P<user>[^\']+)\' logged in from (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$'
        },
        {
            "name": "timestamped_message",
            "regex": r'^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (?P<level>\w+): (?P<message>.*)$'
        },
        {
            "name": "simple_level_message",
            "regex": r'^(?P<level>\w+): (?P<message>.*)$'
        },
        {
            "name": "key_value_pairs",
            "regex": r'^(?P<key1>\w+)=(?P<value1>\S+)\s+(?P<key2>\w+)=(?P<value2>\S+)$'
        }
    ]

    def __init__(self):
        self._compiled_patterns = []
        for p in self.PATTERNS:
            self._compiled_patterns.append({
                "name": p["name"],
                "regex": re.compile(p["regex"])
            })

    def harmonize_line(self, line: str) -> dict:
        """
        Attempts to match a single log line against known patterns and returns a structured dict.
        """
        for pattern_info in self._compiled_patterns:
            match = pattern_info["regex"].match(line)
            if match:
                result = match.groupdict()
                result["_pattern_name"] = pattern_info["name"]
                return result
        
        # If no pattern matches
        return {"raw_message": line.strip(), "_pattern_name": "unmatched"}

    def harmonize_logs(self, log_lines):
        """
        Processes an iterable of log lines and yields harmonized JSON objects.
        """
        for line in log_lines:
            yield self.harmonize_line(line.strip())

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Glitch-Weaver Log Harmonizer: Transforms unstructured log lines into JSON."
    )
    parser.add_argument(
        "log_file",
        nargs="?", # Makes the argument optional
        help="Path to the log file to harmonize. If not provided, reads from stdin."
    )
    args = parser.parse_args()

    harmonizer = LogHarmonizer()

    if args.log_file:
        try:
            with open(args.log_file, 'r', encoding='utf-8') as f:
                for harmonized_data in harmonizer.harmonize_logs(f):
                    print(json.dumps(harmonized_data))
        except FileNotFoundError:
            print(f"Error: Log file '{args.log_file}' not found.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error processing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        for harmonized_data in harmonizer.harmonize_logs(sys.stdin):
            print(json.dumps(harmonized_data))

if __name__ == "__main__":
    main()
