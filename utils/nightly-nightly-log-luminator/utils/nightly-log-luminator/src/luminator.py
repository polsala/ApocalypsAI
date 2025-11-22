import re
import sys
from collections import defaultdict

def get_default_patterns():
    """Returns a dictionary of default regex patterns for common log issues."""
    return {
        "ERROR": r"\bERROR\b",
        "WARNING": r"\bWARNING\b",
        "EXCEPTION": r"\bEXCEPTION\b",
        "CRITICAL": r"\bCRITICAL\b",
        "FAILED": r"\bFAILED\b",
        "DENIED": r"\bDENIED\b",
        "TIMEOUT": r"\bTIMEOUT\b",
        "FATAL": r"\bFATAL\b"
    }

def scan_log_content(log_content: str, patterns: dict) -> tuple[dict, list]:
    """
    Scans log content for defined patterns and identifies anomalous lines.

    Args:
        log_content: The entire content of the log file as a string.
        patterns: A dictionary where keys are pattern names and values are regex strings.

    Returns:
        A tuple containing:
        - A dictionary with counts for each detected pattern.
        - A list of lines that did not match any pattern (anomalies).
    """
    pattern_counts = defaultdict(int)
    anomalous_lines = []
    compiled_patterns = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in patterns.items()}

    lines = log_content.splitlines()
    for line in lines:
        if not line.strip(): # Skip empty lines
            continue

        matched = False
        for name, compiled_pattern in compiled_patterns.items():
            if compiled_pattern.search(line):
                pattern_counts[name] += 1
                matched = True
                break # Only count a line once for the first matching pattern
        if not matched:
            anomalous_lines.append(line)

    return dict(pattern_counts), anomalous_lines

def main():
    """Main function to run the Log Luminator utility."""
    if len(sys.argv) < 2:
        print("Usage: python3 src/luminator.py <path_to_log_file>")
        sys.exit(1)

    log_filepath = sys.argv[1]

    try:
        with open(log_filepath, 'r', encoding='utf-8') as f:
            log_content = f.read()
    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{log_filepath}': {e}")
        sys.exit(1)

    patterns = get_default_patterns()
    pattern_counts, anomalous_lines = scan_log_content(log_content, patterns)

    print("\n--- Log Luminator Report ---")
    print(f"\nScanning: {log_filepath}\n")

    if pattern_counts:
        print("Detected Patterns:")
        # Sort patterns for consistent output
        for name, count in sorted(pattern_counts.items()):
            print(f"  {name}: {count} {'occurrences' if count > 1 else 'occurrence'}")
    else:
        print("No known patterns detected.")

    if anomalous_lines:
        print(f"\nAnomalous Lines ({len(anomalous_lines)} total):")
        # Limit to first 10 anomalous lines for brevity in report
        for i, line in enumerate(anomalous_lines):
            if i >= 10: # Only show first 10 anomalies in report
                print(f"  ... ({len(anomalous_lines) - 10} more anomalies not shown)")
                break
            print(f"  - {line}")
    else:
        print("No anomalous lines detected.")

    print("\n--- End Report ---")

if __name__ == "__main__":
    main()
