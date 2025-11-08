import argparse
import re
from datetime import datetime, timedelta
import sys

class TemporalAnomalyDetector:
    # Common timestamp regex patterns. Add more as needed.
    # The 'timestamp' named group is crucial for extraction.
    DEFAULT_TIMESTAMP_PATTERNS = [
        re.compile(r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d{3,6})?)'), # YYYY-MM-DD HH:MM:SS[.ms/us]
        re.compile(r'(?P<timestamp>\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})'), # MM/DD/YYYY HH:MM:SS
        re.compile(r'\[(?P<timestamp>\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]'), # Apache common log format
        re.compile(r'(?P<timestamp>[A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2})'), # Linux syslog-like (e.g., 'Jan 1 12:00:00') - year assumed current
    ]

    def __init__(self, custom_format_regex=None, temporal_jump_threshold_seconds=3600):
        self.timestamp_patterns = []
        if custom_format_regex:
            try:
                self.timestamp_patterns.append(re.compile(custom_format_regex))
                # Ensure custom regex has the named group
                if 'timestamp' not in self.timestamp_patterns[0].groupindex:
                    raise ValueError("Custom regex must contain a named group 'timestamp', e.g., '(?P<timestamp>...)'")
            except re.error as e:
                raise ValueError(f"Invalid custom regex pattern: {e}")
        self.timestamp_patterns.extend(self.DEFAULT_TIMESTAMP_PATTERNS)

        self.temporal_jump_threshold = timedelta(seconds=temporal_jump_threshold_seconds)

    def _parse_timestamp(self, timestamp_str):
        # Try parsing with common formats. Add more as needed.
        # This is simplified; a robust solution might use dateutil.parser
        formats = [
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%d/%b/%Y:%H:%M:%S %z", # Apache format
            "%b %d %H:%M:%S", # Syslog-like, assumes current year
        ]
        for fmt in formats:
            try:
                # For syslog-like, assume current year if not present
                if fmt == "%b %d %H:%M:%S":
                    current_year = datetime.now().year
                    return datetime.strptime(f"{timestamp_str} {current_year}", f"%b %d %H:%M:%S %Y")
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
        return None # Could not parse

    def detect_anomalies(self, content_source):
        anomalies = []
        last_timestamp = None
        line_num = 0

        # Handle both file paths and file-like objects
        if isinstance(content_source, str):
            try:
                with open(content_source, 'r') as f:
                    lines = f.readlines()
            except FileNotFoundError:
                print(f"Error: File not found at '{content_source}'", file=sys.stderr)
                return []
        else:
            lines = content_source.readlines()

        for line in lines:
            line_num += 1
            current_timestamp_str = None
            for pattern in self.timestamp_patterns:
                match = pattern.search(line)
                if match:
                    current_timestamp_str = match.group('timestamp')
                    break

            if current_timestamp_str:
                current_timestamp = self._parse_timestamp(current_timestamp_str)

                if current_timestamp is None:
                    anomalies.append({
                        'type': 'IMPOSSIBLE_DATE',
                        'line': line_num,
                        'context': line.strip(),
                        'details': f"Could not parse timestamp: '{current_timestamp_str}'"
                    })
                    continue

                if last_timestamp:
                    # Check for out-of-order
                    if current_timestamp < last_timestamp:
                        anomalies.append({
                            'type': 'OUT_OF_ORDER',
                            'line': line_num,
                            'context': line.strip(),
                            'details': f"Current timestamp ({current_timestamp}) is before previous ({last_timestamp})"
                        })
                    # Check for temporal jump
                    elif current_timestamp - last_timestamp > self.temporal_jump_threshold:
                        anomalies.append({
                            'type': 'TEMPORAL_JUMP',
                            'line': line_num,
                            'context': line.strip(),
                            'details': f"Time jump of {current_timestamp - last_timestamp} detected. Previous: {last_timestamp}, Current: {current_timestamp}"
                        })
                last_timestamp = current_timestamp

        return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies in log files."
    )
    parser.add_argument(
        '--file', 
        type=str, 
        required=True, 
        help='Path to the log file to analyze.'
    )
    parser.add_argument(
        '--threshold', 
        type=int, 
        default=3600, 
        help='Maximum allowed time difference (seconds) between consecutive entries before flagging a temporal jump. Default: 3600 (1 hour).'
    )
    parser.add_argument(
        '--format', 
        type=str, 
        help='Custom regex pattern for timestamp extraction. Must contain a named group `(?P<timestamp>...)`.'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Print more detailed information about each anomaly.'
    )

    args = parser.parse_args()

    try:
        detector = TemporalAnomalyDetector(
            custom_format_regex=args.format,
            temporal_jump_threshold_seconds=args.threshold
        )
        anomalies = detector.detect_anomalies(args.file)

        if not anomalies:
            print("No temporal anomalies detected. All clear!")
        else:
            print(f"Detected {len(anomalies)} temporal anomalies:")
            for anomaly in anomalies:
                print(f"  Type: {anomaly['type']}")
                print(f"  Line: {anomaly['line']}")
                print(f"  Context: {anomaly['context']}")
                if args.verbose:
                    print(f"  Details: {anomaly['details']}")
                print("-" * 20)

    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
