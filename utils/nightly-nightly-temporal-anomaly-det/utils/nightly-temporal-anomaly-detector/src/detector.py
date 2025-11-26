import os
import time
import datetime
import argparse
import fnmatch
from typing import List, Tuple, Dict

def get_file_timestamps(filepath: str) -> Tuple[float, float]:
    """
    Retrieves the modification and creation timestamps of a file.
    Returns (mtime, ctime) as Unix timestamps.
    """
    try:
        stat_info = os.stat(filepath)
        return stat_info.st_mtime, stat_info.st_ctime
    except OSError:
        return 0.0, 0.0 # File not found or inaccessible

def detect_anomalies(
    target_dir: str,
    future_threshold_seconds: int,
    stale_threshold_days: int,
    creation_ref_date: datetime.date,
    exclude_patterns: List[str],
    verbose: bool = False
) -> Dict[str, List[str]]:
    """
    Scans the target directory for temporal anomalies in files.

    Args:
        target_dir: The directory to scan.
        future_threshold_seconds: Files modified more than this many seconds in the future.
        stale_threshold_days: Files not modified in this many days.
        creation_ref_date: Files created before this date.
        exclude_patterns: List of glob patterns to exclude files/directories.
        verbose: If True, print more details.

    Returns:
        A dictionary categorizing detected anomalies.
    """
    anomalies = {
        "future_modified": [],
        "ancient_artifacts": [],
        "pre_genesis_creations": [],
    }

    current_time_unix = time.time()
    stale_threshold_unix = current_time_unix - (stale_threshold_days * 24 * 60 * 60)
    creation_ref_unix = datetime.datetime(
        creation_ref_date.year, creation_ref_date.month, creation_ref_date.day,
        tzinfo=datetime.timezone.utc # Assume UTC for reference date
    ).timestamp()

    for root, dirs, files in os.walk(target_dir):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(os.path.join(root, d), p) for p in exclude_patterns)]

        for filename in files:
            filepath = os.path.join(root, filename)

            # Check if file itself should be excluded
            if any(fnmatch.fnmatch(filepath, p) for p in exclude_patterns):
                continue

            mtime, ctime = get_file_timestamps(filepath)

            # Future Modified
            if mtime > current_time_unix + future_threshold_seconds:
                anomalies["future_modified"].append(
                    f"{filepath} (Modified: {datetime.datetime.fromtimestamp(mtime)} > Current: {datetime.datetime.fromtimestamp(current_time_unix)})"
                )

            # Ancient Artifacts
            if mtime < stale_threshold_unix and mtime != 0.0: # mtime 0.0 means file not found/inaccessible
                anomalies["ancient_artifacts"].append(
                    f"{filepath} (Last modified: {datetime.datetime.fromtimestamp(mtime)})"
                )

            # Pre-Genesis Creations (only if ctime is available and meaningful)
            # ctime can be unreliable/platform-dependent, but we'll use it if it exists
            if ctime != 0.0 and ctime < creation_ref_unix:
                anomalies["pre_genesis_creations"].append(
                    f"{filepath} (Created: {datetime.datetime.fromtimestamp(ctime)})"
                )
    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="🌌 Nightly Temporal Anomaly Detector 🌌\n"
                    "Scans directories for files with unusual timestamps.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "target_directory",
        help="The path to the directory you wish to scan for temporal anomalies."
    )
    parser.add_argument(
        "--future-threshold",
        type=int,
        default=60,
        help="Files modified more than this many seconds in the future will be flagged. Default: 60 (1 minute)."
    )
    parser.add_argument(
        "--stale-threshold",
        type=int,
        default=365,
        help="Files not modified in this many days will be flagged as ancient artifacts. Default: 365 (1 year)."
    )
    parser.add_argument(
        "--creation-ref-date",
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d').date(),
        default=datetime.date(2023, 1, 1),
        help="Files created before this date (YYYY-MM-DD) will be flagged as pre-genesis. Default: 2023-01-01."
    )
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="A comma-separated list of glob patterns to exclude files or directories (e.g., '*.log,node_modules/*')."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed information about detected anomalies."
    )

    args = parser.parse_args()

    exclude_patterns = [p.strip() for p in args.exclude.split(',') if p.strip()]

    print(f"Scanning '{args.target_directory}' for temporal anomalies...")
    anomalies = detect_anomalies(
        args.target_directory,
        args.future_threshold,
        args.stale_threshold,
        args.creation_ref_date,
        exclude_patterns,
        args.verbose
    )

    found_anomalies = False
    for category, items in anomalies.items():
        if items:
            found_anomalies = True
            print(f"\n--- {category.replace('_', ' ').title()} ---")
            for item in items:
                print(f"  - {item}")

    if not found_anomalies:
        print("\n✨ No temporal anomalies detected. Your filesystem is chronologically sound! ✨")
    else:
        print("\n🚨 Temporal anomalies detected! Consider investigating these chronological oddities. 🚨")
        exit(1) # Indicate failure if anomalies are found

if __name__ == "__main__":
    main()
