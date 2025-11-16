import argparse
import collections
import os
import sys

def _analyze_file(filepath: str, keywords: list[str], threshold: float, window_size: int) -> list[dict]:
    """
    Analyzes a single log file for keyword density anomalies using a sliding window.
    """
    anomalies = []
    keywords_lower = [k.lower() for k in keywords]
    
    if not os.path.exists(filepath):
        print(f"Warning: Log file not found: {filepath}", file=sys.stderr)
        return anomalies

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            line_buffer = collections.deque(maxlen=window_size)
            line_number = 0
            keyword_count_in_window = 0

            for line in f:
                line_number += 1
                is_keyword_line = any(k in line.lower() for k in keywords_lower)

                # Add new line to buffer and update count
                line_buffer.append((line_number, is_keyword_line))
                if is_keyword_line:
                    keyword_count_in_window += 1

                # If buffer is full, check for anomaly and remove oldest line's impact
                if len(line_buffer) == window_size:
                    current_density = keyword_count_in_window / window_size
                    if current_density >= threshold:
                        start_line = line_buffer[0][0]
                        end_line = line_buffer[-1][0]
                        anomalies.append({
                            'file': filepath,
                            'start_line': start_line,
                            'end_line': end_line,
                            'density': current_density,
                            'message': f"High keyword density ({current_density:.2%}) detected."
                        })
                    
                    # Remove oldest line from consideration
                    oldest_line_info = line_buffer[0]
                    if oldest_line_info[1]: # If oldest line contained a keyword
                        keyword_count_in_window -= 1

            # Check for anomalies in the last partial window if it's smaller than window_size
            # This handles cases where the file is shorter than window_size or ends with a partial window.
            if 0 < len(line_buffer) <= window_size:
                current_density = keyword_count_in_window / len(line_buffer)
                if current_density >= threshold:
                    start_line = line_buffer[0][0]
                    end_line = line_buffer[-1][0]
                    anomalies.append({
                        'file': filepath,
                        'start_line': start_line,
                        'end_line': end_line,
                        'density': current_density,
                        'message': f"High keyword density ({current_density:.2%}) detected in partial window."
                    })

    except IOError as e:
        print(f"Error reading file {filepath}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred while processing {filepath}: {e}", file=sys.stderr)

    return anomalies

def scan_logs(log_paths: list[str], keywords: list[str], threshold: float, window_size: int) -> list[dict]:
    """
    Scans multiple log files for anomalies.
    """
    all_anomalies = []
    print(f"Starting cosmic dust collection across {len(log_paths)} files...")
    for path in log_paths:
        print(f"Scanning log file: {path}")
        file_anomalies = _analyze_file(path, keywords, threshold, window_size)
        if file_anomalies:
            all_anomalies.extend(file_anomalies)
        else:
            print(f"  No significant cosmic dust detected in {path}.")
    return all_anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans log files for keyword density anomalies."
    )
    parser.add_argument(
        '--log-paths', 
        nargs='+', 
        required=True, 
        help='Space-separated list of log file paths to scan.'
    )
    parser.add_argument(
        '--keywords', 
        nargs='+', 
        required=True, 
        help='Space-separated list of keywords to search for (case-insensitive).'
    )
    parser.add_argument(
        '--threshold', 
        type=float, 
        default=0.05, 
        help='The percentage threshold (0.0 to 1.0) of keyword occurrences within a window to flag as an anomaly. Default: 0.05 (5%).'
    )
    parser.add_argument(
        '--window-size', 
        type=int, 
        default=50, 
        help='The number of lines in the sliding window for anomaly detection. Default: 50.'
    )

    args = parser.parse_args()

    if not (0.0 <= args.threshold <= 1.0):
        print("Error: Threshold must be between 0.0 and 1.0.", file=sys.stderr)
        sys.exit(1)
    if args.window_size <= 0:
        print("Error: Window size must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    anomalies = scan_logs(args.log_paths, args.keywords, args.threshold, args.window_size)

    if anomalies:
        print("\n--- Cosmic Dust Report ---")
        for anomaly in anomalies:
            print(f"  Anomaly in {anomaly['file']} (lines {anomaly['start_line']}-{anomaly['end_line']}): {anomaly['message']}")
        sys.exit(1) # Exit with 1 to indicate anomalies were found (non-zero for potential issues)
    else:
        print("\nNo significant cosmic dust detected. All clear!")
        sys.exit(0)

if __name__ == '__main__':
    main()
