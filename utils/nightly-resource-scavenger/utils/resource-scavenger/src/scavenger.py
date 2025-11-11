import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath: str) -> float:
    """Returns the age of a file in days."""
    try:
        mtime = os.path.getmtime(filepath)
        return (time.time() - mtime) / (60 * 60 * 24)
    except (FileNotFoundError, OSError):
        return -1.0 # Indicate error or non-existent file

def get_file_size_mb(filepath: str) -> float:
    """Returns the size of a file in megabytes."""
    try:
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    except (FileNotFoundError, OSError):
        return 0.0 # Indicate error or non-existent file

def scan_directory(
    path: str,
    size_threshold_mb: int = 50,
    age_threshold_days: int = 365,
) -> list[str]:
    """Scans a directory for oversized files, ancient artifacts, and void zones."""
    findings = []
    if not os.path.isdir(path):
        return [f"Error: Path '{path}' is not a valid directory."]

    current_time = time.time()

    for root, dirs, files in os.walk(path):
        # Check for empty directories (void zones)
        # Only flag if it's not the root path itself and it's truly empty
        if not dirs and not files and root != path:
            findings.append(f"[VOID ZONE] {root}/")

        for file in files:
            filepath = os.path.join(root, file)
            
            # Oversized File Detection
            file_size_mb = get_file_size_mb(filepath)
            if file_size_mb > size_threshold_mb:
                findings.append(f"[OVERSIZED FILE] {filepath} ({file_size_mb:.1f} MB)")
            
            # Ancient Artifact Identification
            try:
                mtime = os.path.getmtime(filepath)
                file_age_days = (current_time - mtime) / (60 * 60 * 24)
                if file_age_days > age_threshold_days:
                    last_modified_date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                    findings.append(f"[ANCIENT ARTIFACT] {filepath} (Last modified: {last_modified_date})")
            except (FileNotFoundError, OSError):
                # File might have been deleted between os.walk and os.path.getmtime, or other access error
                pass

    return findings

def main():
    parser = argparse.ArgumentParser(
        description="Resource Scavenger: Identify and reclaim valuable space within your repository."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan."
    )
    parser.add_argument(
        "--size-threshold-mb",
        type=int,
        default=50,
        help="Files larger than this (in MB) will be flagged. Default: 50"
    )
    parser.add_argument(
        "--age-threshold-days",
        type=int,
        default=365,
        help="Files not modified in this many days will be flagged. Default: 365"
    )

    args = parser.parse_args()

    print("--- Resource Scavenger Report ---\n")
    findings = scan_directory(args.path, args.size_threshold_mb, args.age_threshold_days)
    if findings:
        for finding in findings:
            print(finding)
    else:
        print("No significant resource findings. Your repository is surprisingly resilient!")
    print("\n--- Scavenging complete. Your repository is slightly less doomed. ---")

if __name__ == "__main__":
    main()
