import os
import time
import argparse
from datetime import datetime, timedelta

def get_threshold_datetime(mode: str, value: int, unit: str) -> datetime:
    """Calculates the datetime threshold based on mode, value, and unit."""
    now = datetime.now()
    delta = timedelta()

    if unit == 'days':
        delta = timedelta(days=value)
    elif unit == 'hours':
        delta = timedelta(hours=value)
    elif unit == 'minutes':
        delta = timedelta(minutes=value)
    else:
        raise ValueError(f"Unsupported time unit: {unit}")

    if mode == 'older-than':
        return now - delta
    elif mode == 'newer-than':
        # For 'newer-than', we want files *after* this point in time.
        # So, the threshold is 'now - delta', and we look for mtime > threshold.
        return now - delta
    else:
        raise ValueError(f"Unsupported mode: {mode}")

def detect_anomalies(directory: str, mode: str, value: int, unit: str) -> list[str]:
    """Detects files with anomalous modification times in the given directory."""
    anomalous_files = []
    try:
        threshold_dt = get_threshold_datetime(mode, value, unit)
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_dt = datetime.fromtimestamp(mtime_timestamp)

                if mode == 'older-than':
                    if mtime_dt < threshold_dt:
                        anomalous_files.append(filepath)
                elif mode == 'newer-than':
                    if mtime_dt > threshold_dt: # Files newer than (now - delta)
                        anomalous_files.append(filepath)

    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory}'")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    return anomalous_files

def main():
    parser = argparse.ArgumentParser(
        description="A whimsical utility to detect files with 'anomalous' modification times."
    )
    parser.add_argument('--path', type=str, required=True, help='The directory path to scan for temporal anomalies.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--older-than', type=int, help='Detect files older than this value.')
    group.add_argument('--newer-than', type=int, help='Detect files newer than this value.')

    parser.add_argument('unit', choices=['days', 'hours', 'minutes'],
                        help='Unit for the temporal threshold.')

    args = parser.parse_args()

    mode = None
    value = None
    if args.older_than is not None:
        mode = 'older-than'
        value = args.older_than
    elif args.newer_than is not None:
        mode = 'newer-than'
        value = args.newer_than

    if mode and value is not None:
        print(f"Scanning '{args.path}' for files {mode} {value} {args.unit}...")
        anomalies = detect_anomalies(args.path, mode, value, args.unit)
        if anomalies:
            print("\nTemporal Anomalies Detected:")
            for anomaly in anomalies:
                print(f"  - {anomaly}")
        else:
            print("No temporal anomalies detected. All clear!")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
