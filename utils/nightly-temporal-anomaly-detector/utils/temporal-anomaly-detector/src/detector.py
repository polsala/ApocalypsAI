import datetime
import argparse
import sys

def get_local_time() -> datetime.datetime:
    """
    Retrieves the current local system time.
    """
    return datetime.datetime.now()

def get_simulated_ntp_time(base_time: datetime.datetime, offset_seconds: float = 0.0) -> datetime.datetime:
    """
    Simulates fetching time from an NTP server with a given offset.
    In a real-world scenario, this would involve network requests to actual NTP servers.
    """
    return base_time + datetime.timedelta(seconds=offset_seconds)

def check_for_anomalies(
    tolerance_seconds: float,
    ntp_offset_seconds: float = 0.0
) -> tuple[bool, float, datetime.datetime, datetime.datetime]:
    """
    Compares local system time against a simulated NTP time and checks for anomalies.

    Args:
        tolerance_seconds: The maximum acceptable difference in seconds.
        ntp_offset_seconds: Simulated offset for the NTP server's time.

    Returns:
        A tuple: (is_anomaly_detected, drift_seconds, local_time, reference_time)
    """
    local_time = get_local_time()
    reference_time = get_simulated_ntp_time(local_time, ntp_offset_seconds)

    drift = (reference_time - local_time).total_seconds()
    is_anomaly = abs(drift) > tolerance_seconds

    return is_anomaly, drift, local_time, reference_time

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies by comparing local system time with a simulated reference."
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=1.0,
        help="Maximum acceptable time difference in seconds before an anomaly is reported."
    )
    parser.add_argument(
        "--ntp-offset",
        type=float,
        default=0.0,
        help="Simulated offset in seconds for the NTP server's reported time. Positive means NTP is ahead."
    )

    args = parser.parse_args()

    is_anomaly, drift, local_time, reference_time = check_for_anomalies(
        args.tolerance,
        args.ntp_offset
    )

    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Local time: {local_time}")
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Reference time: {reference_time}")

    if is_anomaly:
        status_message = "🚨 TEMPORAL ANOMALY DETECTED! "
        if drift > 0:
            status_message += f"Reference time is {abs(drift):.6f} seconds ahead of local time. 🚨"
        else:
            status_message += f"Reference time is {abs(drift):.6f} seconds behind local time. 🚨"
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Status: {status_message}")
        sys.exit(1) # Exit with non-zero for anomaly detected
    else:
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Status: All temporal vectors aligned. Drift: {drift:.6f} seconds.")
        sys.exit(0) # Exit with zero for no anomaly

if __name__ == "__main__":
    main()
