import os
import time
import argparse
from datetime import datetime, timedelta

def get_file_timestamps(filepath):
    """Returns modification and creation timestamps for a file."""
    try:
        stat = os.stat(filepath)
        # st_mtime: time of most recent content modification
        # st_ctime: time of most recent metadata change (Unix) or creation (Windows)
        mtime = datetime.fromtimestamp(stat.st_mtime)
        ctime = datetime.fromtimestamp(stat.st_ctime)
        return mtime, ctime
    except OSError:
        return None, None

def detect_chronos_drift(
    paths,
    future_threshold_seconds=60,
    past_threshold_seconds=0,
    report_all=False
):
    """Scans specified paths for files with unusual timestamps (chronos drift)."""
    current_time = datetime.now()
    drifted_files = []

    print(f"Scanning for chronos drift in: {', '.join(paths)}")
    print(f"Current system time: {current_time}")
    if future_threshold_seconds > 0:
        print(f"Future drift threshold: {future_threshold_seconds} seconds")
    if past_threshold_seconds > 0:
        print(f"Past drift threshold: {past_threshold_seconds} seconds")

    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: Path not found: {path}")
            continue

        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                mtime, ctime = get_file_timestamps(filepath)

                if mtime is None:
                    print(f"Could not get timestamps for {filepath}")
                    continue

                is_drifted = False
                drift_type = []

                # Check for future drift (mtime)
                if future_threshold_seconds > 0 and mtime > current_time + timedelta(seconds=future_threshold_seconds):
                    is_drifted = True
                    drift_type.append(f"Future MTime (+{(mtime - current_time).total_seconds():.0f}s)")

                # Check for future drift (ctime)
                if future_threshold_seconds > 0 and ctime > current_time + timedelta(seconds=future_threshold_seconds):
                    is_drifted = True
                    drift_type.append(f"Future CTime (+{(ctime - current_time).total_seconds():.0f}s)")

                # Check for significantly past drift (mtime)
                if past_threshold_seconds > 0 and mtime < current_time - timedelta(seconds=past_threshold_seconds):
                    is_drifted = True
                    drift_type.append(f"Past MTime (-{(current_time - mtime).total_seconds():.0f}s)")

                # Check for significantly past drift (ctime)
                if past_threshold_seconds > 0 and ctime < current_time - timedelta(seconds=past_threshold_seconds):
                    is_drifted = True
                    drift_type.append(f"Past CTime (-{(current_time - ctime).total_seconds():.0f}s)")

                if is_drifted or report_all:
                    status = "DRIFTED" if is_drifted else "OK"
                    drift_info = f" [{', '.join(drift_type)}]" if drift_type else ""
                    print(f"[{status}]{drift_info} MTime: {mtime}, CTime: {ctime} -> {filepath}")
                    if is_drifted:
                        drifted_files.append(filepath)

    return drifted_files

def main():
    parser = argparse.ArgumentParser(
        description="Detects files with unusual or 'drifted' timestamps."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--future-threshold",
        type=int,
        default=60,
        help="Files modified/created more than this many seconds in the future will be flagged. Default: 60."
    )
    parser.add_argument(
        "--past-threshold",
        type=int,
        default=0,
        help="Files modified/created more than this many seconds in the past will be flagged. Default: 0 (disabled)."
    )
    parser.add_argument(
        "--report-all",
        action="store_true",
        help="If set, reports all files found, not just those with drift."
    )

    args = parser.parse_args()

    drifted = detect_chronos_drift(
        args.path,
        args.future_threshold,
        args.past_threshold,
        args.report_all
    )

    if drifted:
        print("\n--- Chronos Drift Detected ---")
        for f in drifted:
            print(f)
        print(f"Total drifted files: {len(drifted)}")
        exit(1) # Indicate failure if drift is found
    else:
        print("\nNo chronos drift detected. All timestamps appear stable.")
        exit(0)

if __name__ == "__main__":
    main()
