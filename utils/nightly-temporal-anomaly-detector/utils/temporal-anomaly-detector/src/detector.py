import os
import datetime
import argparse
import sys

def get_current_time():
    """Returns the current UTC datetime."""
    return datetime.datetime.now(datetime.timezone.utc)

def get_file_mtime(filepath):
    """Returns the modification time of a file as a UTC datetime object."""
    try:
        timestamp = os.path.getmtime(filepath)
        return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc)
    except OSError:
        return None # File might have been deleted or permissions issue

def detect_anomalies(directory, ancient_threshold_years=5):
    """
    Detects temporal anomalies (future or ancient modification times) in files.

    Args:
        directory (str): The root directory to scan.
        ancient_threshold_years (int): Files older than this many years are flagged as ancient.

    Returns:
        dict: A dictionary containing lists of 'future_anomalies' and 'ancient_anomalies'.
    """
    future_anomalies = []
    ancient_anomalies = []
    current_time = get_current_time()
    ancient_threshold_date = current_time - datetime.timedelta(days=ancient_threshold_years * 365.25) # Account for leap years

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.", file=sys.stderr)
        return {'future_anomalies': [], 'ancient_anomalies': []}

    print(f"Scanning directory: {directory}")

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            mtime = get_file_mtime(filepath)

            if mtime is None:
                # print(f"Warning: Could not get mtime for {filepath}. Skipping.")
                continue

            if mtime > current_time:
                future_anomalies.append({
                    'filepath': filepath,
                    'modified_time': mtime.isoformat(),
                    'current_time': current_time.isoformat(),
                    'type': 'Future Anomaly'
                })
            elif mtime < ancient_threshold_date:
                ancient_anomalies.append({
                    'filepath': filepath,
                    'modified_time': mtime.isoformat(),
                    'current_time': current_time.isoformat(),
                    'type': 'Ancient Anomaly'
                })
            # else:
                # print(f"No anomalies detected for: {filepath}")

    return {
        'future_anomalies': future_anomalies,
        'ancient_anomalies': ancient_anomalies
    }

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies (future or ancient file modification times) in a directory."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='The root directory to scan for temporal anomalies.'
    )
    parser.add_argument(
        '--ancient-threshold', 
        type=int, 
        default=5, 
        help='Files older than this many years will be flagged as ancient. Default is 5.'
    )

    args = parser.parse_args()

    print(f"\n--- Temporal Anomaly Report ---\n")

    results = detect_anomalies(args.path, args.ancient_threshold)

    if results['future_anomalies']:
        print("Future Anomalies:")
        for anomaly in results['future_anomalies']:
            print(f"  - {anomaly['filepath']} (Modified: {anomaly['modified_time']}, Current: {anomaly['current_time']})")
        print()
    else:
        print("No Future Anomalies detected.")
        print()

    if results['ancient_anomalies']:
        print(f"Ancient Anomalies (threshold: {args.ancient_threshold} years):")
        for anomaly in results['ancient_anomalies']:
            print(f"  - {anomaly['filepath']} (Modified: {anomaly['modified_time']}, Current: {anomaly['current_time']})")
        print()
    else:
        print(f"No Ancient Anomalies detected (threshold: {args.ancient_threshold} years).")
        print()

    if not results['future_anomalies'] and not results['ancient_anomalies']:
        print("Congratulations! No temporal anomalies found in the scanned directory.")

    print("--- Scan Complete ---")


if __name__ == '__main__':
    main()
