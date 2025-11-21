import os
import datetime
import time

def detect_anomalies(root_dir: str, current_timestamp: float, stale_threshold_seconds: float) -> dict:
    """
    Detects temporal anomalies in files within a given directory.

    Anomalies include:
    - Files with modification times in the future.
    - Files considered "stale" (modification time older than a threshold).

    Args:
        root_dir (str): The root directory to scan.
        current_timestamp (float): The current time as a Unix timestamp (e.g., from time.time()).
        stale_threshold_seconds (float): The duration in seconds after which a file is considered stale.

    Returns:
        dict: A dictionary containing lists of paths for 'future_modified_files' and 'stale_files'.
    """
    anomalies = {
        "future_modified_files": [],
        "stale_files": [],
    }

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                mtime = os.path.getmtime(filepath)

                # Anomaly 1: Future modified files
                if mtime > current_timestamp:
                    anomalies["future_modified_files"].append(filepath)

                # Anomaly 2: Stale files
                if (current_timestamp - mtime) > stale_threshold_seconds:
                    anomalies["stale_files"].append(filepath)

            except FileNotFoundError:
                # File might have been deleted between os.walk and os.path.getmtime
                # or is otherwise inaccessible. Skip it gracefully.
                continue
            except Exception as e:
                # Catch other potential errors during stat operations
                print(f"Warning: Could not process {filepath}: {e}")
                continue
    return anomalies

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies (future or stale modification times) in files."
    )
    parser.add_argument("path", help="The root directory to scan for anomalies.")
    parser.add_argument(
        "--stale-days",
        type=int,
        default=365,
        help="Number of days after which a file is considered stale (default: 365 days).",
    )
    args = parser.parse_args()

    root_path = args.path
    stale_threshold_seconds = args.stale_days * 24 * 60 * 60
    current_timestamp = time.time()

    print(f"Scanning '{root_path}' for temporal anomalies...")
    print(f"Current time: {datetime.datetime.fromtimestamp(current_timestamp)}")
    print(f"Stale threshold: {args.stale_days} days")

    results = detect_anomalies(root_path, current_timestamp, stale_threshold_seconds)

    if not any(results.values()):
        print("\nNo temporal anomalies detected. All clear!")
    else:
        print("\n--- Temporal Anomaly Report ---")
        if results["future_modified_files"]:
            print("\nFuture Modified Files (mtime > current time):")
            for f in results["future_modified_files"]:
                # Re-get mtime for printing, in case it changed (unlikely in this context)
                # or if the original mtime was just a mock value in tests.
                try:
                    mtime_str = datetime.datetime.fromtimestamp(os.path.getmtime(f))
                except FileNotFoundError:
                    mtime_str = "[File not found]"
                print(f"- {f} (mtime: {mtime_str})")
        if results["stale_files"]:
            print(f"\nStale Files (mtime older than {args.stale_days} days):")
            for f in results["stale_files"]:
                try:
                    mtime_str = datetime.datetime.fromtimestamp(os.path.getmtime(f))
                except FileNotFoundError:
                    mtime_str = "[File not found]"
                print(f"- {f} (mtime: {mtime_str})")
        print("\n--- End Report ---")

if __name__ == "__main__":
    main()
