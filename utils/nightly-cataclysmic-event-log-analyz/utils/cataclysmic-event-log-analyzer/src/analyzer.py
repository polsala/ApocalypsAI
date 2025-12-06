import argparse
import os

class LogAnalyzer:
    def __init__(self):
        # Keywords are ordered by severity for deterministic priority if multiple exist on one line
        self.keywords = {
            'CRITICAL': 'CRITICAL',
            'FATAL': 'CRITICAL',
            'APOCALYPSE': 'CRITICAL', # Whimsical keyword
            'DOOM': 'CRITICAL',      # Whimsical keyword
            'ERROR': 'ERROR',
            'FAILURE': 'ERROR',
            'WARNING': 'WARNING'
        }

    def analyze_log_content(self, log_content: str, filename: str = 'unknown_log') -> list:
        events = []
        lines = log_content.splitlines()
        for i, line in enumerate(lines):
            for keyword, level in self.keywords.items():
                if keyword.lower() in line.lower():
                    events.append({
                        'filename': filename,
                        'line_num': i + 1,
                        'level': level,
                        'message': line.strip()
                    })
                    break # Only report the first matching keyword per line (based on dict order)
        return events

    def parse_log_file(self, filepath: str) -> list:
        if not os.path.exists(filepath):
            print(f"Error: Log file not found at '{filepath}'")
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.analyze_log_content(content, os.path.basename(filepath))
        except Exception as e:
            print(f"Error reading file '{filepath}': {e}")
            return []

def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files for cataclysmic events (errors, warnings, critical messages)."
    )
    parser.add_argument(
        'log_files', metavar='LOG_FILE', type=str, nargs='+',
        help='One or more paths to log files to analyze.'
    )

    args = parser.parse_args()

    analyzer = LogAnalyzer()
    all_events = []

    for log_file in args.log_files:
        all_events.extend(analyzer.parse_log_file(log_file))

    if not all_events:
        print("No potential cataclysmic events detected.")
        return

    print("\n--- Cataclysmic Event Report ---")
    print(f"\nDetected {len(all_events)} potential cataclysmic events:\n")

    for event in all_events:
        print(f"[{event['filename']}:L{event['line_num']}] {event['level']}: {event['message']}")

    print("\n--- End Report ---")

if __name__ == '__main__':
    main()
