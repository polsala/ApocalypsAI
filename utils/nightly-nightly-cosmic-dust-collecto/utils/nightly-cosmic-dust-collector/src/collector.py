import argparse
import os
import re
from collections import defaultdict

def collect_dust(root_path: str, patterns: list[str]) -> dict:
    """
    Scans log files in a given root_path for specified patterns and summarizes anomalies.

    Args:
        root_path: The root directory to start scanning for log files.
        patterns: A list of string patterns to search for in log lines.

    Returns:
        A dictionary containing the scan results.
    """
    results = {
        "total_files_scanned": 0,
        "total_lines_scanned": 0,
        "total_anomalies_found": 0,
        "unique_anomaly_lines": set(),
        "pattern_counts": defaultdict(int),
        "files_with_anomalies": set()
    }

    if not os.path.isdir(root_path):
        print(f"Error: Directory not found at '{root_path}'")
        return results

    compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.log'):
                file_path = os.path.join(dirpath, filename)
                results["total_files_scanned"] += 1
                file_has_anomalies = False

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            results["total_lines_scanned"] += 1
                            for pattern_str, compiled_pattern in zip(patterns, compiled_patterns):
                                if compiled_pattern.search(line):
                                    results["total_anomalies_found"] += 1
                                    results["pattern_counts"][pattern_str] += 1
                                    results["unique_anomaly_lines"].add(line.strip())
                                    file_has_anomalies = True
                                    break # Only count one pattern match per line for simplicity
                except Exception as e:
                    print(f"Warning: Could not read file '{file_path}': {e}")
                
                if file_has_anomalies:
                    results["files_with_anomalies"].add(file_path)

    results["unique_anomaly_lines"] = sorted(list(results["unique_anomaly_lines"]))
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Scan log files for specified patterns and summarize anomalies."
    )
    parser.add_argument(
        "--path", 
        required=True, 
        help="The root directory to start scanning for log files."
    )
    parser.add_argument(
        "--patterns", 
        nargs='*', 
        default=['ERROR', 'FAIL', 'Exception', 'Traceback'],
        help="One or more patterns to search for. Defaults to ['ERROR', 'FAIL', 'Exception', 'Traceback']."
    )

    args = parser.parse_args()

    print(f"\n--- Nightly Cosmic Dust Collector Report ---")
    print(f"Scanning directory: {args.path}")
    print(f"Searching for patterns: {', '.join(args.patterns)}\n")

    scan_results = collect_dust(args.path, args.patterns)

    print(f"Total files scanned: {scan_results['total_files_scanned']}")
    print(f"Total lines scanned: {scan_results['total_lines_scanned']}")
    print(f"Total anomalies found: {scan_results['total_anomalies_found']}")
    print(f"Files with anomalies: {len(scan_results['files_with_anomalies'])}")

    if scan_results['total_anomalies_found'] > 0:
        print("\n--- Anomaly Summary ---")
        for pattern, count in scan_results['pattern_counts'].items():
            print(f"  '{pattern}' occurrences: {count}")
        
        print("\n--- Unique Anomaly Lines (first 10) ---")
        for i, line in enumerate(scan_results['unique_anomaly_lines']):
            if i >= 10: # Limit output for brevity
                print(f"  ... ({len(scan_results['unique_anomaly_lines']) - 10} more unique lines)")
                break
            print(f"  - {line}")
        
        print("\n--- Files Containing Anomalies ---")
        for i, file_path in enumerate(scan_results['files_with_anomalies']):
            if i >= 5: # Limit output for brevity
                print(f"  ... ({len(scan_results['files_with_anomalies']) - 5} more files)")
                break
            print(f"  - {file_path}")
    else:
        print("\nNo cosmic dust (anomalies) found. All clear!")

    print(f"\n--- End of Report ---")


if __name__ == "__main__":
    main()
