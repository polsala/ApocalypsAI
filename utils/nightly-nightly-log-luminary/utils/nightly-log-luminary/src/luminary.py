import sys
from collections import Counter

def analyze_log(log_file_path):
    """
    Analyzes a log file to summarize key information.
    Counts total lines, specific keywords (ERROR, WARNING, INFO),
    and identifies the top 5 most frequent lines.
    """
    total_lines = 0
    error_count = 0
    warning_count = 0
    info_count = 0
    line_counts = Counter()

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1
                stripped_line = line.strip()
                if not stripped_line: # Skip empty lines for frequency count and keyword check
                    continue

                line_counts[stripped_line] += 1

                upper_line = stripped_line.upper()
                if 'ERROR' in upper_line:
                    error_count += 1
                elif 'WARNING' in upper_line:
                    warning_count += 1
                elif 'INFO' in upper_line:
                    info_count += 1

    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"--- Log Analysis Report for '{log_file_path}' ---")
    print(f"Total Lines Processed: {total_lines}")
    print(f"Errors Found: {error_count}")
    print(f"Warnings Found: {warning_count}")
    print(f"Info Messages Found: {info_count}")
    print("\nTop 5 Most Frequent Lines:")
    if line_counts:
        for line, count in line_counts.most_common(5):
            print(f"  - [Count: {count}] {line}")
    else:
        print("  (No unique non-empty lines found)")
    print("--------------------------------------------------")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python src/luminary.py <path_to_log_file>", file=sys.stderr)
        sys.exit(1)

    log_file = sys.argv[1]
    analyze_log(log_file)
