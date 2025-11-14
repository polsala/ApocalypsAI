import argparse
import re
import os

DEFAULT_PATTERNS = [
    r"ERROR",
    r"CRITICAL",
    r"FAIL(ED)?",
    r"DENIED",
    r"WARNING",
    r"exception",
    r"segfault",
    r"panic",
    r"unauthorized",
    r"timeout",
    r"corrupt",
    r"malformed"
]

def load_patterns(patterns_file_path):
    """Loads anomaly patterns from a specified file."""
    if not os.path.exists(patterns_file_path):
        raise FileNotFoundError(f"Patterns file not found: {patterns_file_path}")

    patterns = []
    with open(patterns_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                patterns.append(line)
    return patterns

def analyze_log(log_file_path, patterns):
    """Scans a log file for specified anomaly patterns and reports findings."""
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Log file not found: {log_file_path}")

    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    anomalies_found = []

    with open(log_file_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            for pattern in compiled_patterns:
                if pattern.search(line):
                    anomalies_found.append({
                        "line_number": line_num,
                        "content": line.strip(),
                        "matched_pattern": pattern.pattern
                    })
                    break # Only report one match per line to avoid duplicates for multiple patterns
    return anomalies_found

def main():
    parser = argparse.ArgumentParser(
        description="Whispers of the Void Log Analyzer: Detects anomalies in log files."
    )
    parser.add_argument(
        "--log-file",
        required=True,
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--patterns-file",
        help="Optional path to a custom patterns file. Defaults to internal patterns if not provided."
    )

    args = parser.parse_args()

    try:
        if args.patterns_file:
            patterns = load_patterns(args.patterns_file)
            if not patterns:
                print(f"Warning: No patterns loaded from '{args.patterns_file}'. Using default patterns.")
                patterns = DEFAULT_PATTERNS
        else:
            patterns = DEFAULT_PATTERNS

        if not patterns:
            print("Error: No anomaly patterns defined. Exiting.")
            return 1

        print(f"Analyzing log file: {args.log_file} with {len(patterns)} patterns...")
        anomalies = analyze_log(args.log_file, patterns)

        if anomalies:
            print("\n--- Anomalies Detected ---")
            for anomaly in anomalies:
                print(f"Line {anomaly['line_number']} (Pattern: '{anomaly['matched_pattern']}'): {anomaly['content']}")
            print("--------------------------")
            print(f"Total anomalies: {len(anomalies)}")
            return 0 # Indicate success with anomalies found
        else:
            print("No anomalies detected. All clear.")
            return 0 # Indicate success with no anomalies

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
