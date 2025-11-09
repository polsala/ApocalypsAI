import os
import datetime
import argparse
from typing import List, Dict

def get_file_mtime(filepath: str) -> datetime.datetime:
    """Returns the modification time of a file as a datetime object."""
    return datetime.datetime.fromtimestamp(os.path.getmtime(filepath))

def scan_for_anomalies(
    directory: str,
    max_age_days: int,
    min_age_seconds: int
) -> Dict[str, List[str]]:
    """
    Scans a directory for files with temporal anomalies.

    Args:
        directory: The path to the directory to scan.
        max_age_days: Files older than this (in days) are considered "too old".
        min_age_seconds: Files newer than this (in seconds) are considered "too new".

    Returns:
        A dictionary with 'too_old' and 'too_new' lists of file paths.
    """
    anomalies = {"too_old": [], "too_new": []}
    now = datetime.datetime.now()
    
    # Calculate thresholds
    old_threshold = now - datetime.timedelta(days=max_age_days)
    new_threshold = now - datetime.timedelta(seconds=min_age_seconds) # Files newer than this are "too new"

    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return anomalies

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                mtime = get_file_mtime(filepath)
                if mtime < old_threshold:
                    anomalies["too_old"].append(f"{filepath} (Modified: {mtime.isoformat()})")
                elif mtime > new_threshold: # Check if file is newer than the 'new' threshold
                    anomalies["too_new"].append(f"{filepath} (Modified: {mtime.isoformat()})")
            except FileNotFoundError:
                # File might have been deleted between os.walk and get_file_mtime
                continue
            except Exception as e:
                print(f"Warning: Could not process {filepath}: {e}")

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for files with temporal anomalies (too old or too new)."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan."
    )
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=30,
        help="Files older than this many days are flagged as 'too old'. Default: 30"
    )
    parser.add_argument(
        "--min-age-seconds",
        type=int,
        default=5,
        help="Files newer than this many seconds are flagged as 'too new'. Default: 5"
    )
    args = parser.parse_args()

    print(f"Scanning '{args.directory}' for temporal anomalies...")
    print(f"  Max age for 'too old': {args.max_age_days} days")
    print(f"  Min age for 'too new': {args.min_age_seconds} seconds")

    anomalies = scan_for_anomalies(
        args.directory,
        args.max_age_days,
        args.min_age_seconds
    )

    if anomalies["too_old"] or anomalies["too_new"]:
        print("\n--- Temporal Anomalies Detected! ---")
        if anomalies["too_old"]:
            print("\nFiles that are suspiciously old:")
            for f in anomalies["too_old"]:
                print(f"- {f}")
        if anomalies["too_new"]:
            print("\nFiles that are surprisingly new:")
            for f in anomalies["too_new"]:
                print(f"- {f}")
        exit(1) # Indicate anomalies found
    else:
        print("\nNo temporal anomalies detected. All clear!")
        exit(0) # Indicate no anomalies

if __name__ == "__main__":
    main()
