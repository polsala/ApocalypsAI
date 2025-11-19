import datetime
import argparse
import sys

def get_system_time():
    """Returns the current system time as a datetime object, aware of UTC."""
    return datetime.datetime.now(datetime.timezone.utc)

def get_mock_reference_time():
    """Mock reference time provider for testing and demonstration.
    In a real-world scenario, this would fetch time from an NTP server or a similar trusted source.
    """
    # Mock rationale: This function serves as a placeholder for a network call
    # to an NTP server. For deterministic, offline tests, it returns a fixed time.
    # In a production environment, this would be replaced with actual NTP client logic
    # (e.g., using the 'ntplib' library).
    return datetime.datetime(2023, 10, 27, 10, 0, 0, tzinfo=datetime.timezone.utc)

def check_time_drift(reference_time_provider, threshold_seconds):
    """
    Checks the system time against a reference time and reports drift.

    Args:
        reference_time_provider (callable): A function that returns a timezone-aware
                                            datetime object representing the trusted reference time.
        threshold_seconds (int): The maximum acceptable time drift in seconds.

    Returns:
        tuple: (drift_seconds, message) where drift_seconds is the difference
               in seconds (system_time - reference_time) and message is a string.
    """
    system_time = get_system_time()
    reference_time = reference_time_provider()

    drift = system_time - reference_time
    drift_seconds = drift.total_seconds()

    if abs(drift_seconds) > threshold_seconds:
        if drift_seconds > 0:
            message = f"WARNING: System clock is ahead by {drift_seconds:.2f} seconds (>{threshold_seconds}s threshold)."
        else:
            message = f"WARNING: System clock is behind by {abs(drift_seconds):.2f} seconds (>{threshold_seconds}s threshold)."
        return drift_seconds, message
    else:
        message = f"INFO: System clock is within {threshold_seconds} seconds of reference. Drift: {drift_seconds:.2f} seconds."
        return drift_seconds, message

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chrono-Sync Beacon: Detects system clock drift."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1,
        help="Maximum acceptable time drift in seconds (default: 1)",
    )
    args = parser.parse_args()

    drift_seconds, message = check_time_drift(get_mock_reference_time, args.threshold)
    print(message)

    if abs(drift_seconds) > args.threshold:
        sys.exit(1) # Exit with error code if drift exceeds threshold
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
