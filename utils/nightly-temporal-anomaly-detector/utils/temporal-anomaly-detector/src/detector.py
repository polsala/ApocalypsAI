import os
import sys
import time
import argparse
import re
from datetime import datetime, timedelta

def get_current_time_epoch():
    """# Mock rationale: Allows deterministic testing of age calculations."""
    return time.time()

def get_file_mtime_epoch(path):
    """# Mock rationale: Allows deterministic testing of file modification times."""
    return os.path.getmtime(path)

def path_exists(path):
    """# Mock rationale: Allows deterministic testing of path existence."""
    return os.path.exists(path)

def is_directory(path):
    """# Mock rationale: Allows deterministic testing of path type."""
    return os.path.isdir(path)

def list_directory_contents(path):
    """# Mock rationale: Allows deterministic testing of directory contents."""
    return os.listdir(path)

def detect_anomalies(path, max_age_seconds=None, expected_patterns=None, verbose=False):
    anomalies = []
    current_time = get_current_time_epoch()

    if not path_exists(path):
        anomalies.append(f"Temporal Anomaly: Path '{path}' has vanished from existence!")
        return anomalies

    if is_directory(path):
        if verbose:
            print(f"Monitoring directory: {path}")
        contents = list_directory_contents(path)
        if not contents:
            if verbose:
                print(f"Directory '{path}' is empty.")
            return anomalies

        for item_name in contents:
            item_path = os.path.join(path, item_name)
            if is_directory(item_path): # Skip subdirectories for simplicity
                if verbose:
                    print(f"Skipping subdirectory: {item_path}")
                continue

            # Check age
            if max_age_seconds is not None:
                mtime = get_file_mtime_epoch(item_path)
                age_seconds = current_time - mtime
                if age_seconds > max_age_seconds:
                    anomalies.append(
                        f"Temporal Anomaly: File '{item_path}' is {age_seconds:.0f} seconds old "
                        f"(>{max_age_seconds}s). It's ancient!"
                    )
                elif verbose:
                    print(f"File '{item_path}' is {age_seconds:.0f} seconds old (OK).")

            # Check pattern
            if expected_patterns:
                matched = False
                for pattern in expected_patterns:
                    if re.match(pattern, item_name):
                        matched = True
                        break
                if not matched:
                    anomalies.append(
                        f"Temporal Anomaly: File '{item_path}' does not match any expected pattern. "
                        f"A rogue entity has appeared!"
                    )
                elif verbose:
                    print(f"File '{item_path}' matches expected patterns (OK).")
            elif verbose:
                print(f"File '{item_path}' (no pattern check specified).")

    else: # It's a file
        if verbose:
            print(f"Monitoring file: {path}")
        # Check age
        if max_age_seconds is not None:
            mtime = get_file_mtime_epoch(path)
            age_seconds = current_time - mtime
            if age_seconds > max_age_seconds:
                anomalies.append(
                    f"Temporal Anomaly: File '{path}' is {age_seconds:.0f} seconds old "
                    f"(>{max_age_seconds}s). It's ancient!"
                )
            elif verbose:
                print(f"File '{path}' is {age_seconds:.0f} seconds old (OK).")
        elif verbose:
            print(f"File '{path}' (no age check specified).")

        # Pattern check is not applicable for a single file path itself, only its name if part of a dir.
        # We could add a check for the file's name against patterns, but for a single file, 
        # the primary check is existence and age.

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Temporal Anomaly Detector: Monitor files and directories for spacetime disruptions."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The file or directory path to monitor."
    )
    parser.add_argument(
        "--max-age-days",
        type=float,
        help="Report a file as an anomaly if its last modification time is older than this many days."
    )
    parser.add_argument(
        "--expect-pattern",
        action="append",
        help="For directories: A regex pattern that all expected filenames should match. "
             "Files not matching will be reported as anomalies. Can be specified multiple times."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print more detailed information, even for non-anomalous items."
    )

    args = parser.parse_args()

    max_age_seconds = None
    if args.max_age_days is not None:
        max_age_seconds = args.max_age_days * 24 * 60 * 60

    anomalies = detect_anomalies(
        args.path,
        max_age_seconds=max_age_seconds,
        expected_patterns=args.expect_pattern,
        verbose=args.verbose
    )

    if anomalies:
        print("\n--- Temporal Anomalies Detected! ---")
        for anomaly in anomalies:
            print(f"- {anomaly}")
        print("-------------------------------------\n")
        sys.exit(1)
    else:
        if args.verbose:
            print("\n--- All clear. Spacetime continuum stable. ---")
        else:
            print("No temporal anomalies detected.")
        sys.exit(0)

if __name__ == "__main__":
    main()
