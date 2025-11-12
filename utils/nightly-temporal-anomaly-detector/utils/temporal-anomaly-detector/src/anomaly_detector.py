import os
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any

def get_file_timestamps(filepath: str) -> Dict[str, datetime]:
    """
    Retrieves creation and modification timestamps for a given file.
    Returns them as datetime objects.
    """
    try:
        stat = os.stat(filepath)
        # On some systems (e.g., Linux), ctime is the last metadata change time,
        # not creation time. For cross-platform consistency, we'll use it as
        # a proxy for "creation" but acknowledge its limitations.
        # mtime is consistently modification time.
        return {
            "ctime": datetime.fromtimestamp(stat.st_ctime),
            "mtime": datetime.fromtimestamp(stat.st_mtime),
        }
    except OSError:
        return {"ctime": datetime.min, "mtime": datetime.min} # Indicate error

def detect_anomalies(
    scan_path: str,
    future_threshold_hours: int = 24,
    past_threshold_years: int = 10,
    verbose: bool = False
) -> List[Dict[str, Any]]:
    """
    Scans a directory for temporal anomalies in file timestamps.

    Anomalies include:
    1. Modification time is before creation time.
    2. Timestamp is significantly in the future.
    3. Timestamp is significantly in the past.
    """
    anomalies: List[Dict[str, Any]] = []
    now = datetime.now()
    future_limit = now + timedelta(hours=future_threshold_hours)
    past_limit = now - timedelta(days=past_threshold_years * 365) # Approximate years

    print(f"Scanning '{scan_path}' for temporal anomalies...")
    print(f"  Future threshold: > {future_threshold_hours} hours from now ({future_limit.strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"  Past threshold: < {past_threshold_years} years from now ({past_limit.strftime('%Y-%m-%d %H:%M:%S')})")
    print("-" * 40)

    for root, _, files in os.walk(scan_path):
        for file in files:
            filepath = os.path.join(root, file)
            timestamps = get_file_timestamps(filepath)
            ctime = timestamps["ctime"]
            mtime = timestamps["mtime"]

            file_anomalies = []

            # Anomaly 1: Modification before creation
            if mtime < ctime:
                file_anomalies.append("Modification time is before creation time")

            # Anomaly 2: Future timestamp
            if ctime > future_limit:
                file_anomalies.append(f"Creation time is in the future ({ctime.strftime('%Y-%m-%d %H:%M:%S')})")
            if mtime > future_limit:
                file_anomalies.append(f"Modification time is in the future ({mtime.strftime('%Y-%m-%d %H:%M:%S')})")

            # Anomaly 3: Past timestamp
            if ctime < past_limit and ctime != datetime.min: # Exclude error case
                file_anomalies.append(f"Creation time is significantly in the past ({ctime.strftime('%Y-%m-%d %H:%M:%S')})")
            if mtime < past_limit and mtime != datetime.min: # Exclude error case
                file_anomalies.append(f"Modification time is significantly in the past ({mtime.strftime('%Y-%m-%d %H:%M:%S')})")

            if file_anomalies:
                anomalies.append({
                    "filepath": filepath,
                    "ctime": ctime.strftime('%Y-%m-%d %H:%M:%S'),
                    "mtime": mtime.strftime('%Y-%m-%d %H:%M:%S'),
                    "anomalies": file_anomalies
                })
                print(f"🚨 ANOMALY DETECTED: {filepath}")
                print(f"  Ctime: {ctime.strftime('%Y-%m-%d %H:%M:%S')}, Mtime: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                for anomaly_msg in file_anomalies:
                    print(f"  - {anomaly_msg}")
                print("-" * 40)
            elif verbose:
                print(f"✅ Normal: {filepath}")
                print(f"  Ctime: {ctime.strftime('%Y-%m-%d %H:%M:%S')}, Mtime: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
                print("-" * 40)

    if not anomalies:
        print("✨ No temporal anomalies detected. Your timeline is pristine!")
    else:
        print(f"\nSummary: {len(anomalies)} temporal anomalies found.")

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies in file timestamps within a directory."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for temporal anomalies."
    )
    parser.add_argument(
        "--future-threshold-hours",
        type=int,
        default=24,
        help="Files with timestamps more than this many hours in the future will be flagged. Default: 24."
    )
    parser.add_argument(
        "--past-threshold-years",
        type=int,
        default=10,
        help="Files with timestamps more than this many years in the past will be flagged. Default: 10."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print details for all scanned files, not just anomalies."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: The provided path '{args.path}' is not a valid directory.")
        exit(1)

    anomalies = detect_anomalies(
        args.path,
        args.future_threshold_hours,
        args.past_threshold_years,
        args.verbose
    )

    if anomalies:
        exit(1) # Indicate that anomalies were found
    else:
        exit(0) # Indicate success (no anomalies)

if __name__ == "__main__":
    main()
