import argparse
import re
import sys
from collections import defaultdict

class LogAnalyzer:
    def __init__(self):
        self.patterns = {
            "DEBUG": re.compile(r".*DEBUG.*", re.IGNORECASE),
            "INFO": re.compile(r".*INFO.*", re.IGNORECASE),
            "WARNING": re.compile(r".*WARN(ING)?.*", re.IGNORECASE),
            "ERROR": re.compile(r".*ERROR.*", re.IGNORECASE),
            "CRITICAL": re.compile(r".*CRITICAL.*|.*FATAL.*", re.IGNORECASE),
        }
        self.severity_weights = {
            "DEBUG": 0,
            "INFO": 0,
            "WARNING": 2,
            "ERROR": 5,
            "CRITICAL": 10,
        }

    def analyze(self, log_content):
        line_count = 0
        level_counts = defaultdict(int)
        error_details = defaultdict(list)
        total_gloom_points = 0

        for line in log_content.splitlines():
            line_count += 1
            matched = False
            for level, pattern in self.patterns.items():
                if pattern.search(line):
                    level_counts[level] += 1
                    total_gloom_points += self.severity_weights.get(level, 0)
                    if level in ["WARNING", "ERROR", "CRITICAL"]:
                        error_details[level].append(line.strip())
                    matched = True
                    break
            if not matched: # Count lines that don't match any specific level as INFO by default
                level_counts["INFO"] += 1

        # Calculate Gloom-Glimmer Score
        # Score is 100 - (total gloom points / max possible gloom points) * 100
        # Max possible gloom points if every line was CRITICAL
        max_gloom_points = line_count * self.severity_weights["CRITICAL"]
        
        gloom_score = 0
        if line_count > 0 and max_gloom_points > 0:
            gloom_score = (total_gloom_points / max_gloom_points) * 100
        
        glimmer_score = max(0, 100 - gloom_score) # Ensure score is not negative

        return {
            "total_lines": line_count,
            "level_counts": dict(level_counts),
            "error_details": dict(error_details),
            "gloom_glimmer_score": round(glimmer_score, 2)
        }

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Glimmer Log Analyzer: Scans log files and provides a system health score."
    )
    parser.add_argument("log_file", help="Path to the log file to analyze.")
    args = parser.parse_args()

    try:
        with open(args.log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"Error: Log file not found at '{args.log_file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}", file=sys.stderr)
        sys.exit(1)

    analyzer = LogAnalyzer()
    report = analyzer.analyze(log_content)

    print("\n--- Gloom-Glimmer Log Analysis Report ---")
    print(f"Total Lines: {report['total_lines']}")
    print("\nLog Level Counts:")
    for level, count in report['level_counts'].items():
        print(f"  {level}: {count}")

    print("\nError/Warning Details:")
    if not report['error_details']:
        print("  No significant gloom detected. Keep up the good work!")
    else:
        for level, messages in report['error_details'].items():
            print(f"  {level} ({len(messages)} occurrences):")
            for msg in messages[:5]: # Show first 5 messages for brevity
                print(f"    - {msg}")
            if len(messages) > 5:
                print(f"    ... and {len(messages) - 5} more.")

    print(f"\n--- Gloom-Glimmer Score: {report['gloom_glimmer_score']}/100 ---")
    if report['gloom_glimmer_score'] >= 80:
        print("System is shining bright! Minimal gloom detected.")
    elif report['gloom_glimmer_score'] >= 50:
        print("System is holding steady, but some shadows linger. Keep an eye out!")
    else:
        print("System is feeling a bit gloomy. Time for some serious troubleshooting!")

if __name__ == "__main__":
    main()
