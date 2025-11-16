import os
import time
import argparse
from collections import defaultdict

def scan_logs(directory: str, time_window_hours: int = 24) -> dict:
    """
    Scans log files in the given directory for error patterns within a specified time window.

    Args:
        directory: The path to the directory containing log files.
        time_window_hours: The time window in hours to consider log files.

    Returns:
        A dictionary containing scan results: files scanned, total errors, and error details.
    """
    error_keywords = ["ERROR", "FAIL", "EXCEPTION", "CRITICAL", "FATAL"]
    log_files_scanned = 0
    total_error_lines = 0
    error_details = defaultdict(int)

    current_time = time.time()
    time_threshold = current_time - (time_window_hours * 3600) # Convert hours to seconds

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return {
            "files_scanned": 0,
            "total_error_lines": 0,
            "error_details": {}
        }

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(('.log', '.txt')):
                file_path = os.path.join(root, file_name)
                try:
                    # Check if file was modified within the time window
                    if os.path.getmtime(file_path) < time_threshold:
                        continue # Skip old files

                    log_files_scanned += 1
                    with open(file_path, 'r', errors='ignore') as f:
                        for line in f:
                            for keyword in error_keywords:
                                if keyword in line.upper():
                                    total_error_lines += 1
                                    # Use the full line as the error message for aggregation
                                    error_details[line.strip()] += 1
                                    break # Only count one keyword per line
                except Exception as e:
                    print(f"Warning: Could not read file {file_path}: {e}")

    return {
        "files_scanned": log_files_scanned,
        "total_error_lines": total_error_lines,
        "error_details": dict(error_details)
    }

def summarize_findings(scan_results: dict):
    """
    Prints a summary of the log scan findings.
    """
    print("\nNightly Log Whisperer Report")
    print("----------------------------")

    print(f"\nFiles scanned: {scan_results['files_scanned']}")
    print(f"Total error lines found: {scan_results['total_error_lines']}")

    if scan_results['error_details']:
        sorted_errors = sorted(scan_results['error_details'].items(), key=lambda item: item[1], reverse=True)
        print("\nTop 5 Error Messages:")
        for i, (message, count) in enumerate(sorted_errors[:5]):
            print(f"{i+1}. {message} ({count} occurrences)")
    else:
        print("\nNo significant error whispers detected.")

    print("\nAll clear, for now. Keep whispering!")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Log Whisperer: Scans logs for anomalies."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for log files (e.g., /var/log, ./logs)."
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="The time window in hours to consider log files (e.g., 24 for the last 24 hours)."
    )

    args = parser.parse_args()

    print(f"Scanning directory: {args.path}")
    print(f"Time window: {args.hours} hours")

    results = scan_logs(args.path, args.hours)
    summarize_findings(results)

if __name__ == "__main__":
    main()
