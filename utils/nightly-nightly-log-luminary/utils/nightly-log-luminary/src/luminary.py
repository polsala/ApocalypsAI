import argparse
import re
import sys

def analyze_log(log_file_path: str, patterns: list[str]) -> dict:
    """
    Scans a log file for specified regex patterns and returns a summary of findings.
    """
    results = {
        "total_lines": 0,
        "matches_by_pattern": {pattern: [] for pattern in patterns}
    }

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                results["total_lines"] += 1
                for pattern_str in patterns:
                    if re.search(pattern_str, line):
                        results["matches_by_pattern"][pattern_str].append({
                            "line_number": line_num,
                            "content": line.strip()
                        })
        return results
    except FileNotFoundError:
        print(f"Error: Log file not found at '{log_file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def print_summary(results: dict):
    """
    Prints a formatted summary of the log analysis results.
    """
    print("\n--- Nightly Log Luminary Report ---")
    print(f"Total lines scanned: {results['total_lines']}")
    print("\n--- Findings ---")

    found_any_matches = False
    for pattern, matches in results["matches_by_pattern"].items():
        if matches:
            found_any_matches = True
            print(f"\nPattern: '{pattern}' ({len(matches)} matches)")
            for match in matches:
                print(f"  L{match['line_number']}: {match['content']}")
    
    if not found_any_matches:
        print("No specified patterns found in the log file.")
    
    print("\n--- End of Report ---")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Log Luminary: Scans log files for specified patterns."
    )
    parser.add_argument(
        "log_file",
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "patterns",
        nargs=":", # Use ':' to allow 0 or more patterns, but argparse requires at least one for positional
        default=[], # Default to empty list if no patterns are provided
        help="One or more regex patterns to search for (e.g., 'ERROR', 'WARNING', 'failed')."
    )

    args = parser.parse_args()

    if not args.patterns:
        print("Error: At least one pattern must be provided.", file=sys.stderr)
        sys.exit(1)

    results = analyze_log(args.log_file, args.patterns)
    print_summary(results)

if __name__ == "__main__":
    main()
