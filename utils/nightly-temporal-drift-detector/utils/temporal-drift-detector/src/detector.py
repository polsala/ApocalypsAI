import time
import os
import json
from typing import Optional

# Configuration
LAST_TIME_FILE = ".last_time"
EXPECTED_INTERVAL_SECONDS = 60.0  # Expected time between runs for drift calculation
DRIFT_TOLERANCE_SECONDS = 5.0     # How much deviation from EXPECTED_INTERVAL_SECONDS is allowed

def get_current_timestamp() -> float:
    """Returns the current UTC timestamp."""
    return time.time()

def read_last_timestamp(file_path: str) -> Optional[float]:
    """Reads the last recorded timestamp from a file."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if content:
                return float(content)
    except (ValueError, IOError) as e:
        print(f"[ERROR] Could not read or parse {file_path}: {e}")
    return None

def write_current_timestamp(file_path: str, timestamp: float):
    """Writes the current timestamp to a file."""
    try:
        with open(file_path, 'w') as f:
            f.write(str(timestamp))
    except IOError as e:
        print(f"[ERROR] Could not write to {file_path}: {e}")

def detect_temporal_anomaly(
    last_timestamp: Optional[float],
    current_timestamp: float,
    expected_interval: float,
    drift_tolerance: float
) -> Optional[str]:
    """
    Detects if the current timestamp deviates significantly from the last recorded one,
    considering an expected interval and tolerance.

    Returns a warning/error message if an anomaly is detected, otherwise None.
    """
    if last_timestamp is None:
        return None # No anomaly on first run

    elapsed_time = current_timestamp - last_timestamp
    drift = elapsed_time - expected_interval

    print(f"[INFO] Last recorded time: {last_timestamp}, Current time: {current_timestamp}")
    print(f"[INFO] Expected interval: {expected_interval}s, Actual elapsed: {elapsed_time:.1f}s, Drift: {drift:.1f}s")

    if abs(drift) > drift_tolerance:
        if drift > 0:
            return f"[ERROR] Temporal anomaly detected! Time jumped forward by {drift:.1f} seconds beyond tolerance."
        else:
            return f"[ERROR] Temporal anomaly detected! Time jumped backward by {abs(drift):.1f} seconds beyond tolerance."
    else:
        print("[INFO] Time is within expected bounds.")
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    last_time_file_path = os.path.join(script_dir, LAST_TIME_FILE)

    last_timestamp = read_last_timestamp(last_time_file_path)
    current_timestamp = get_current_timestamp()

    if last_timestamp is None:
        print(f"[INFO] No previous timestamp found. Initializing {LAST_TIME_FILE}.")
    else:
        anomaly_message = detect_temporal_anomaly(
            last_timestamp,
            current_timestamp,
            EXPECTED_INTERVAL_SECONDS,
            DRIFT_TOLERANCE_SECONDS
        )
        if anomaly_message:
            print(anomaly_message)

    write_current_timestamp(last_time_file_path, current_timestamp)
    print(f"[INFO] Current time recorded: {current_timestamp}")

if __name__ == "__main__":
    main()
