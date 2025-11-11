import datetime
import time
import sys

def get_local_time():
    """Returns the current local time as a datetime object."""
    return datetime.datetime.now()

def get_reference_time():
    """
    Simulates getting a reference time from an external source.
    In a real scenario, this would query an NTP server or similar.
    For this utility, it's designed to be easily mocked for testing.
    """
    # Using UTC for a stable 'reference' in mockable scenarios.
    # In a real implementation, you might use a library like `ntplib`
    # to query an actual NTP server or a cloud time service.
    return datetime.datetime.utcnow()

def detect_anomaly(local_time, reference_time, threshold_seconds=5):
    """
    Detects if the local time deviates from the reference time by more than a threshold.
    Returns (is_anomaly, drift_seconds).
    """
    drift = (local_time - reference_time).total_seconds()
    is_anomaly = abs(drift) > threshold_seconds
    return is_anomaly, drift

def main():
    print("Initiating Temporal Anomaly Scan...")
    local_t = get_local_time()
    reference_t = get_reference_time() # This will be mocked in tests

    is_anomaly, drift = detect_anomaly(local_t, reference_t)

    print(f"Local Time: {local_t.isoformat()}")
    print(f"Reference Time: {reference_t.isoformat()} (simulated external source)")
    print(f"Time Drift: {drift:.2f} seconds")

    if is_anomaly:
        print(f"🚨 TEMPORAL ANOMALY DETECTED! Drift of {drift:.2f} seconds exceeds threshold.")
        return 1 # Indicate an anomaly
    else:
        print("✅ All temporal vectors aligned. No anomalies detected.")
        return 0 # Indicate no anomaly

if __name__ == "__main__":
    sys.exit(main())
