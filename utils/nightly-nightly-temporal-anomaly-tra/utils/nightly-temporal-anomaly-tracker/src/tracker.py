import os
import argparse
import datetime
from pathlib import Path
import sys

def get_current_time():
    """Returns the current UTC time."""
    return datetime.datetime.now(datetime.timezone.utc)

def scan_for_anomalies(
    target_path: Path,
    future_threshold_days: int = 0,
    old_threshold_days: int = 365,
):
    """
    Scans the target_path for files with temporal anomalies.

    Args:
        target_path: The path to scan.
        future_threshold_days: Files modified more than this many days in the future are flagged.
        old_threshold_days: Files not modified for more than this many days are flagged as 'ancient'.

    Returns:
        A tuple containing two lists: (future_anomalies, ancient_anomalies).
        Each item in the list is a tuple: (file_path, modification_time, current_time).
    """
    future_anomalies = []
    ancient_anomalies = []
    current_time = get_current_time()

    future_delta = datetime.timedelta(days=future_threshold_days)
    old_delta = datetime.timedelta(days=old_threshold_days)

    print(f"Scanning {target_path} for temporal anomalies...")

    for root, _, files in os.walk(target_path):
        for file_name in files:
            file_path = Path(root) / file_name
            try:
                # Get modification time in UTC
                mod_timestamp = os.path.getmtime(file_path)
                mod_time = datetime.datetime.fromtimestamp(mod_timestamp, datetime.timezone.utc)

                time_difference = mod_time - current_time

                if time_difference > future_delta:
                    future_anomalies.append((file_path, mod_time, current_time))
                elif time_difference < -old_delta:
                    ancient_anomalies.append((file_path, mod_time, current_time))
            except OSError as e:
                print(f"Warning: Could not access {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred with {file_path}: {e}")

    return future_anomalies, ancient_anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for files with temporal anomalies (future or ancient modification times)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory to scan for temporal anomalies."
    )
    parser.add_argument(
        "--future-threshold-days",
        type=int,
        default=0,
        help="Files modified more than this many days in the future are flagged. Default: 0 (any future modification)."
    )
    parser.add_argument(
        "--old-threshold-days",
        type=int,
        default=365,
        help="Files not modified for more than this many days are flagged as 'ancient'. Default: 365."
    )

    args = parser.parse_args()

    target_path = Path(args.path)
    if not target_path.is_dir():
        print(f"Error: Path '{target_path}' is not a valid directory.")
        sys.exit(1)

    future_anomalies, ancient_anomalies = scan_for_anomalies(
        target_path,
        args.future_threshold_days,
        args.old_threshold_days
    )

    print("\n--- Temporal Anomalies Detected ---")

    if future_anomalies:
        print(f"\nFuture Modifications (modified > {args.future_threshold_days} days in the future):")
        for file_path, mod_time, current_time in future_anomalies:
            print(f"  - {file_path} (Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')} UTC, Current: {current_time.strftime('%Y-%m-%d %H:%M:%S')} UTC)")
    else:
        print(f"\nNo future modifications detected (threshold: > {args.future_threshold_days} days in future).")

    if ancient_anomalies:
        print(f"\nAncient Artifacts (not modified for > {args.old_threshold_days} days):")
        for file_path, mod_time, current_time in ancient_anomalies:
            print(f"  - {file_path} (Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')} UTC, Current: {current_time.strftime('%Y-%m-%d %H:%M:%S')} UTC)")
    else:
        print(f"\nNo ancient artifacts detected (threshold: > {args.old_threshold_days} days old).")

    print("\nScan complete.")

    if future_anomalies or ancient_anomalies:
        sys.exit(1) # Indicate anomalies were found
    else:
        sys.exit(0) # Indicate no anomalies

if __name__ == "__main__":
    main()
