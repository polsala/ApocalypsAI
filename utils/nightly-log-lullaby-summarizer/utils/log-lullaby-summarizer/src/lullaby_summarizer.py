import sys
import re
from collections import defaultdict

def summarize_logs(log_file_path: str) -> dict:
    """
    Reads a log file, identifies unique error/warning patterns, and counts their occurrences.

    Args:
        log_file_path: The path to the log file.

    Returns:
        A dictionary where keys are log patterns (e.g., "[ERROR] Message") and values are their counts.
    """
    problem_patterns = defaultdict(int)
    # Regex to capture common log levels and the rest of the line as the message
    # It tries to be flexible with timestamp/prefix, focusing on the level and message.
    log_level_patterns = {
        "CRITICAL": re.compile(r".*(CRITICAL|FATAL):?\s*(.*)"),
        "ERROR": re.compile(r".*(ERROR):?\s*(.*)"),
        "WARNING": re.compile(r".*(WARN|WARNING):?\s*(.*)"),
    }

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                found_match = False
                for level, pattern_re in log_level_patterns.items():
                    match = pattern_re.match(line)
                    if match:
                        # Use the captured message part, clean it up a bit
                        message = match.group(2).strip()
                        # Further clean: remove common prefixes like "logger_name: " or "filename:lineno "
                        message = re.sub(r"^[a-zA-Z0-9_.-]+:\s*", "", message)
                        message = re.sub(r"^[a-zA-Z0-9_.-]+:\d+:\s*", "", message)

                        # Create a standardized pattern string
                        pattern_key = f"[{level.upper()}] {message}"
                        problem_patterns[pattern_key] += 1
                        found_match = True
                        break # Only count the highest severity match per line

        return problem_patterns

    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/lullaby_summarizer.py <path_to_your_log_file>", file=sys.stderr)
        sys.exit(1)

    log_file_path = sys.argv[1]
    summary = summarize_logs(log_file_path)

    print("\n🎶 Log Lullaby Summary 🎶")
    print("--------------------------\n")

    if summary:
        print("After a thorough scan, here are the unique patterns that might need your attention:\n")
        for pattern, count in sorted(summary.items(), key=lambda item: item[1], reverse=True):
            print(f"{pattern} ({count} time{'s' if count > 1 else ''})")
        print("\nAll other logs seem to be resting peacefully. Sweet dreams!")
    else:
        print("No critical errors or warnings detected. Your logs are already sleeping soundly!")
        print("Sweet dreams!")

if __name__ == "__main__":
    main()
