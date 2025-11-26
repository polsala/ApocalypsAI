import argparse
import sys

class LogLuminary:
    def __init__(self):
        self.log_levels = {
            'CRITICAL': 0,
            'ERROR': 0,
            'WARNING': 0,
            'INFO': 0,
            'DEBUG': 0,
            'UNKNOWN': 0
        }
        self.highlight_colors = {
            'CRITICAL': '\033[91m',  # Red
            'ERROR': '\033[91m',     # Red
            'WARNING': '\033[93m',   # Yellow
            'RESET': '\033[0m'       # Reset color
        }
        self.critical_keywords = ['CRITICAL', 'ERROR', 'WARNING']

    def analyze_log(self, file_path):
        total_lines = 0
        log_content = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    total_lines += 1
                    log_content.append(line.rstrip('\n'))
                    detected = False
                    for level in self.log_levels.keys():
                        if level != 'UNKNOWN' and level.lower() in line.lower():
                            self.log_levels[level] += 1
                            detected = True
                            break
                    if not detected:
                        self.log_levels['UNKNOWN'] += 1
            return log_content, total_lines
        except FileNotFoundError:
            print(f"Error: Log file not found at '{file_path}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
            sys.exit(1)

    def generate_report(self, file_path, total_lines):
        report = []
        report.append("\n--- Log Luminary Report ---")
        report.append(f"File: {file_path}")
        report.append("\nSeverity Summary:")
        
        # Sort levels for consistent output, putting known levels first
        # and UNKNOWN last if it has entries.
        sorted_levels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
        final_levels = [level for level in sorted_levels if self.log_levels[level] > 0]
        if self.log_levels['UNKNOWN'] > 0:
            final_levels.append('UNKNOWN')
        elif 'UNKNOWN' in self.log_levels and all(self.log_levels[k] == 0 for k in sorted_levels):
            # If only UNKNOWN lines, still show UNKNOWN
            final_levels.append('UNKNOWN')

        max_len = max(len(level) for level in final_levels) if final_levels else 0

        for level in final_levels:
            report.append(f"  {level:<{max_len}}: {self.log_levels[level]}")
        
        report.append(f"\nTotal Lines Scanned: {total_lines}")
        report.append("\n--- End Report ---")
        return "\n".join(report)

    def print_highlighted_log(self, log_content):
        print("\n--- Highlighted Log Entries ---")
        for line in log_content:
            highlighted_line = line
            for keyword in self.critical_keywords:
                if keyword.lower() in line.lower():
                    color = self.highlight_colors.get(keyword.upper(), self.highlight_colors['RESET'])
                    highlighted_line = f"{color}{line}{self.highlight_colors['RESET']}"
                    break # Highlight only the first critical keyword found per line
            print(highlighted_line)
        print("--- End Highlighted Log ---\n")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files for critical entries and provide a summary."
    )
    parser.add_argument(
        "log_file_path",
        type=str,
        help="The path to the log file to analyze."
    )
    parser.add_argument(
        "--highlight",
        action="store_true",
        help="If present, print the log file with critical lines highlighted."
    )

    args = parser.parse_args()

    luminary = LogLuminary()
    log_content, total_lines = luminary.analyze_log(args.log_file_path)

    print(luminary.generate_report(args.log_file_path, total_lines))

    if args.highlight:
        luminary.print_highlighted_log(log_content)

if __name__ == "__main__":
    main()
