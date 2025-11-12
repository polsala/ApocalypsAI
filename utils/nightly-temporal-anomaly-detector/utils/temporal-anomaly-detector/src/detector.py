import os
import sys
import time
from datetime import datetime

def find_temporal_anomalies(directory_path: str) -> list[str]:
    """
    Scans the specified directory for files with modification timestamps in the future.
    Returns a list of paths to anomalous files.
    """
    anomalies = []
    current_time = time.time()

    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at '{directory_path}'", file=sys.stderr)
        return []

    print(f"Scanning {directory_path} for temporal anomalies...")

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                mtime = os.path.getmtime(file_path)
                if mtime > current_time:
                    anomalies.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}", file=sys.stderr)

    return anomalies

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/detector.py <directory_path>", file=sys.stderr)
        sys.exit(1)

    target_directory = sys.argv[1]
    anomalies = find_temporal_anomalies(target_directory)

    if anomalies:
        for anomaly_path in anomalies:
            # Re-get mtime for printing, in case time.time() changed slightly
            # or for consistency with the original check.
            # In a real scenario, you might store mtime with the path.
            mtime_dt = datetime.fromtimestamp(os.path.getmtime(anomaly_path))
            print(f"Anomaly Detected: {anomaly_path} (Modified: {mtime_dt.strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"\nScan complete. {len(anomalies)} anomalies detected.")
    else:
        print("No temporal anomalies found. The timeline is stable.")
        print("Scan complete. 0 anomalies detected.")

if __name__ == "__main__":
    main()
