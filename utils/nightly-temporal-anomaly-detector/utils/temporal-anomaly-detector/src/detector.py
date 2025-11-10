import os
import datetime
import argparse

def find_temporal_anomalies(path):
    """
    Scans the given path for files with modification times in the future.
    Yields (filepath, mtime_datetime) for each anomaly found.
    """
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directory not found: {path}")

    now = datetime.datetime.now()
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_datetime = datetime.datetime.fromtimestamp(mtime_timestamp)
                if mtime_datetime > now:
                    yield filepath, mtime_datetime
            except OSError as e:
                # Handle cases where file might be deleted or permissions issue
                print(f"Warning: Could not access {filepath}: {e}", file=os.stderr)
                continue

def main():
    parser = argparse.ArgumentParser(
        description="Detects files with future modification times (temporal anomalies)."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The directory to scan for temporal anomalies."
    )
    args = parser.parse_args()

    anomalies_found = False
    print(f"Scanning '{args.path}' for temporal anomalies...")
    try:
        for filepath, mtime in find_temporal_anomalies(args.path):
            print(f"ANOMALY DETECTED: '{filepath}' has future modification time: {mtime}")
            anomalies_found = True
        
        if not anomalies_found:
            print("No temporal anomalies detected. All clear!")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=os.stderr)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=os.stderr)
        exit(1)

if __name__ == "__main__":
    main()
