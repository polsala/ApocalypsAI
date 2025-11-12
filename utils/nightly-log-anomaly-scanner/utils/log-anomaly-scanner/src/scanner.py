import os
import re
import argparse
from typing import List, Dict, Any

def scan_logs(directory_path: str, patterns: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Scans log files in the given directory for specified regex patterns.

    Args:
        directory_path: The path to the directory containing log files.
        patterns: A list of regex patterns to search for.

    Returns:
        A dictionary where keys are filenames and values are lists of dictionaries,
        each representing a detected anomaly with 'line_num', 'line_content', and 'pattern'.
    """
    anomalies: Dict[str, List[Dict[str, Any]]] = {}
    compiled_patterns = [re.compile(p) for p in patterns]

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        return {}

    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        if os.path.isfile(filepath):
            file_anomalies = []
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        for pattern in compiled_patterns:
                            if pattern.search(line):
                                file_anomalies.append({
                                    'line_num': i + 1,
                                    'line_content': line.strip(),
                                    'pattern': pattern.pattern
                                })
                                break # Only report one pattern match per line
                if file_anomalies:
                    anomalies[filename] = file_anomalies
            except Exception as e:
                print(f"Warning: Could not read file '{filepath}': {e}")
    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Scan log files for user-defined regex patterns and report anomalies."
    )
    parser.add_argument(
        "directory",
        help="Path to the directory containing log files."
    )
    parser.add_argument(
        "-p", "--patterns",
        nargs='+',
        required=True,
        help="One or more regex patterns to search for. E.g., 'ERROR' 'WARN' 'failed to connect'"
    )

    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for patterns: {args.patterns}")
    results = scan_logs(args.directory, args.patterns)

    if results:
        print("\n--- Anomaly Report ---")
        for filename, file_anomalies in results.items():
            print(f"\nFile: {filename}")
            for anomaly in file_anomalies:
                print(f"  Line {anomaly['line_num']} (Pattern: '{anomaly['pattern']}'): {anomaly['line_content']}")
        print("\n--- Scan Complete: Anomalies Found! ---")
        exit(1) # Indicate anomalies found
    else:
        print("\n--- Scan Complete: No Anomalies Detected. All clear! ---")
        exit(0) # Indicate no anomalies

if __name__ == "__main__":
    main()
