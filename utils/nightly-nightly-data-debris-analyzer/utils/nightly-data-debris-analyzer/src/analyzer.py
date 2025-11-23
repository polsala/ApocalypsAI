import argparse
from collections import Counter
import re

def analyze_log_file(file_path: str, top_n: int = 5):
    """
    Analyzes a log file to count log levels and identify most frequent unique lines.
    """
    total_lines = 0
    error_count = 0
    warning_count = 0
    info_count = 0
    line_counts = Counter()

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                line = line.strip()
                if not line:
                    continue

                # Count log levels (case-insensitive)
                if re.search(r'ERROR', line, re.IGNORECASE):
                    error_count += 1
                elif re.search(r'WARNING', line, re.IGNORECASE):
                    warning_count += 1
                elif re.search(r'INFO', line, re.IGNORECASE):
                    info_count += 1
                
                # Count unique lines
                line_counts[line] += 1

    except FileNotFoundError:
        print(f"Error: Log file not found at '{file_path}'")
        return
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return

    print(f"--- Log Analysis Report for '{file_path}' ---")
    print(f"Total Lines: {total_lines}")
    print(f"Errors: {error_count}")
    print(f"Warnings: {warning_count}")
    print(f"Info: {info_count}")
    print("\n--- Top Most Frequent Unique Lines ---")

    if line_counts:
        for line, count in line_counts.most_common(top_n):
            print(f"  [Count: {count}] {line}")
    else:
        print("  No unique lines found or file was empty.")

def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files for common log levels and frequent unique lines."
    )
    parser.add_argument(
        "log_file_path",
        type=str,
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top most frequent unique lines to display (default: 5)."
    )
    args = parser.parse_args()

    analyze_log_file(args.log_file_path, args.top)

if __name__ == "__main__":
    main()
