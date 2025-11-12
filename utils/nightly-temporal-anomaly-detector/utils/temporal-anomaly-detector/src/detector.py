import os
import datetime
import argparse

def get_current_time_utc():
    """Helper to get current UTC time. Can be mocked for testing."""
    return datetime.datetime.now(datetime.timezone.utc)

def get_file_mtime_utc(filepath):
    """Helper to get file modification time in UTC. Can be mocked for testing."""
    return datetime.datetime.fromtimestamp(os.path.getmtime(filepath), datetime.timezone.utc)

def find_temporal_anomalies(directory_path, max_age_years=10):
    """
    Scans a directory for files with future or excessively old modification timestamps.

    Args:
        directory_path (str): The path to the directory to scan.
        max_age_years (int): Files older than this threshold will be flagged as ancient.

    Returns:
        list: A list of dictionaries, each representing an anomaly.
              Each dict contains 'type', 'filepath', and 'mtime'.
    """
    anomalies = []
    current_time = get_current_time_utc()
    ancient_threshold = current_time - datetime.timedelta(days=max_age_years * 365) # Simple year calculation

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'")
        return []

    print(f"Temporal Anomaly Report for: {directory_path}\n")

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                mtime = get_file_mtime_utc(filepath)
                
                if mtime > current_time:
                    anomalies.append({
                        'type': 'FUTURE',
                        'filepath': filepath,
                        'mtime': mtime
                    })
                elif mtime < ancient_threshold:
                    anomalies.append({
                        'type': 'ANCIENT',
                        'filepath': filepath,
                        'mtime': mtime
                    })
            except OSError as e:
                print(f"Warning: Could not access file '{filepath}': {e}")
            except Exception as e:
                print(f"Warning: An unexpected error occurred with '{filepath}': {e}")

    for anomaly in anomalies:
        print(f"[{anomaly['type']}] {anomaly['filepath']} (Modified: {anomaly['mtime'].strftime('%Y-%m-%d %H:%M:%S')})")

    print(f"\nScan complete. {len(anomalies)} anomalies found.")
    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects files with future or excessively old modification timestamps."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The root directory to scan for temporal anomalies."
    )
    parser.add_argument(
        "--max-age-years",
        type=int,
        default=10,
        help="Files older than this threshold (in years) will be flagged as ancient. Default is 10."
    )
    args = parser.parse_args()

    find_temporal_anomalies(args.directory_path, args.max_age_years)

if __name__ == "__main__":
    main()
