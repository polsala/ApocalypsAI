import os
import datetime
import time
import argparse

DEFAULT_FUTURE_THRESHOLD_DAYS = 7
DEFAULT_PAST_THRESHOLD_DAYS = 30

def scan_directory(
    path: str,
    future_threshold_days: int = DEFAULT_FUTURE_THRESHOLD_DAYS,
    past_threshold_days: int = DEFAULT_PAST_THRESHOLD_DAYS
) -> list[tuple[str, datetime.datetime, str]]:
    """
    Scans a directory for files with modification times outside specified thresholds.

    Args:
        path: The root directory to scan.
        future_threshold_days: Max days into the future for mtime.
        past_threshold_days: Max days into the past for mtime.

    Returns:
        A list of tuples: (filepath, mtime_datetime, anomaly_type).
    """
    anomalies = []
    current_utc_dt = datetime.datetime.now(datetime.timezone.utc)

    future_limit_dt = current_utc_dt + datetime.timedelta(days=future_threshold_days)
    past_limit_dt = current_utc_dt - datetime.timedelta(days=past_threshold_days)

    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_dt = datetime.datetime.fromtimestamp(mtime_timestamp, tz=datetime.timezone.utc)

                if mtime_dt > future_limit_dt:
                    anomalies.append((filepath, mtime_dt, "FUTURE ANOMALY"))
                elif mtime_dt < past_limit_dt:
                    anomalies.append((filepath, mtime_dt, "PAST ANOMALY"))
            except OSError as e:
                # Handle cases where file might be deleted between walk and getmtime, or permissions issues
                print(f"Warning: Could not access {filepath} - {e}")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

    return anomalies

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies (future/past modification times) in files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--future-threshold",
        type=int,
        default=DEFAULT_FUTURE_THRESHOLD_DAYS,
        help=f"Number of days into the future a file's mtime can be. Default: {DEFAULT_FUTURE_THRESHOLD_DAYS}"
    )
    parser.add_argument(
        "--past-threshold",
        type=int,
        default=DEFAULT_PAST_THRESHOLD_DAYS,
        help=f"Number of days into the past a file's mtime can be. Default: {DEFAULT_PAST_THRESHOLD_DAYS}"
    )

    args = parser.parse_args()

    print(f"Scanning directory: {args.path}")

    anomalies = scan_directory(
        args.path,
        args.future_threshold,
        args.past_threshold
    )

    if anomalies:
        print("\n--- Temporal Anomalies Detected ---")
        for filepath, mtime_dt, anomaly_type in anomalies:
            delta = abs(datetime.datetime.now(datetime.timezone.utc) - mtime_dt)
            print(f"[{anomaly_type}] {filepath} (Modified: {mtime_dt.strftime('%Y-%m-%d %H:%M:%S UTC')})")
            print(f"  Rationale: File's modification time is {delta.days} days {'in the future' if anomaly_type == 'FUTURE ANOMALY' else 'in the past'}.")
    else:
        print("\nNo temporal anomalies detected. All clear!")

    print("\n--- Scan Complete ---")
    print(f"Total anomalies found: {len(anomalies)}")

if __name__ == "__main__":
    main()
