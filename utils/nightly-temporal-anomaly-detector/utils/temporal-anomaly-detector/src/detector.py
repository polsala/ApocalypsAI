import os
import argparse
import datetime
import time

def get_file_times(filepath):
    """
    Retrieves modification time (mtime) and metadata change time (ctime) for a file.
    Returns (mtime_timestamp, ctime_timestamp) or (None, None) if error.
    """
    try:
        stat_info = os.stat(filepath)
        return stat_info.st_mtime, stat_info.st_ctime
    except OSError:
        return None, None

def format_timestamp(timestamp):
    """Formats a Unix timestamp into a human-readable datetime string."""
    if timestamp is None:
        return "N/A"
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def scan_directory_for_anomalies(path, threshold_seconds=86400):
    """
    Scans a directory recursively for files with temporal anomalies.
    An anomaly is defined as:
    1. The absolute difference between mtime and ctime exceeds threshold_seconds.
    2. mtime is older than ctime by more than 1 second (a specific "time warp" anomaly).
    """
    anomalies = []
    for root, _, files in os.walk(path):
        for filename in files:
            filepath = os.path.join(root, filename)
            mtime, ctime = get_file_times(filepath)

            if mtime is None or ctime is None:
                # Skip files we couldn't stat (e.g., permission issues, broken symlinks)
                continue

            diff = mtime - ctime

            # Anomaly Type 1: Large absolute difference
            if abs(diff) > threshold_seconds:
                anomaly_type = "large absolute difference"
                if diff < 0:
                    anomaly_type = "mtime significantly older than ctime"
                elif diff > 0:
                    anomaly_type = "mtime significantly newer than ctime"
                anomalies.append({
                    "path": filepath,
                    "mtime": mtime,
                    "ctime": ctime,
                    "diff": diff,
                    "type": anomaly_type
                })
            # Anomaly Type 2: mtime is older than ctime (more specific "time warp")
            # This catches cases where diff is negative but might be within threshold_seconds
            # but still represents a potential issue (e.g., mtime = 10:00, ctime = 10:05, diff = -300s)
            elif diff < -1: # Use -1 to account for minor system clock variations
                 anomalies.append({
                    "path": filepath,
                    "mtime": mtime,
                    "ctime": ctime,
                    "diff": diff,
                    "type": "mtime older than ctime (potential time warp)"
                })

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for temporal anomalies in file modification and metadata change times."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The directory path to scan for anomalies."
    )
    parser.add_argument(
        "--threshold-seconds",
        type=int,
        default=86400, # 24 hours
        help="The maximum allowed absolute difference between mtime and ctime in seconds. Default is 86400 (24 hours)."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.")
        exit(1)

    print(f"Scanning '{args.path}' for temporal anomalies with a threshold of {args.threshold_seconds} seconds...")
    anomalies = scan_directory_for_anomalies(args.path, args.threshold_seconds)

    if anomalies:
        print("\n--- Detected Temporal Anomalies ---")
        for anomaly in anomalies:
            print(f"[ANOMALY] {anomaly['path']}: "
                  f"mtime={format_timestamp(anomaly['mtime'])}, "
                  f"ctime={format_timestamp(anomaly['ctime'])}, "
                  f"Diff={anomaly['diff']:.1f}s ({anomaly['type']})")
        exit(0) # Indicate anomalies found
    else:
        print("\nNo temporal anomalies detected. All clear!")
        exit(2) # Indicate no anomalies (no-op)

if __name__ == "__main__":
    main()
