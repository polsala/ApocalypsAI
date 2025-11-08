import datetime
import ntplib
import sys
import argparse

DEFAULT_NTP_SERVER = 'pool.ntp.org'
DEFAULT_THRESHOLD_SECONDS = 5.0

def get_ntp_time(server: str) -> datetime.datetime | None:
    """Queries an NTP server and returns its UTC time as a datetime object."""
    client = ntplib.NTPClient()
    try:
        print(f"[Temporal Anomaly Detector] Attempting to query NTP server: {server}")
        response = client.request(server, version=3)
        # ntplib response.tx_time is a float representing seconds since epoch
        ntp_utc_timestamp = response.tx_time
        return datetime.datetime.fromtimestamp(ntp_utc_timestamp, tz=datetime.timezone.utc)
    except (ntplib.NTPException, ConnectionRefusedError, TimeoutError, OSError) as e:
        print(f"[Temporal Anomaly Detector] Error: Could not query NTP server '{server}'. {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Detects temporal anomalies (system clock drift) by comparing local time with an NTP server."
    )
    parser.add_argument(
        '--server', 
        type=str, 
        default=DEFAULT_NTP_SERVER, 
        help=f"NTP server to query (default: {DEFAULT_NTP_SERVER})"
    )
    parser.add_argument(
        '--threshold', 
        type=float, 
        default=DEFAULT_THRESHOLD_SECONDS, 
        help=f"Time difference threshold in seconds to consider an anomaly (default: {DEFAULT_THRESHOLD_SECONDS}s)"
    )
    args = parser.parse_args()

    local_utc = datetime.datetime.now(datetime.timezone.utc)
    print(f"[Temporal Anomaly Detector] Local UTC: {local_utc.isoformat(timespec='microseconds')}")

    ntp_utc = get_ntp_time(args.server)

    if ntp_utc is None:
        print("[Temporal Anomaly Detector] Status: Failed to check for anomalies due to NTP server error.", file=sys.stderr)
        sys.exit(2)

    time_diff = abs((local_utc - ntp_utc).total_seconds())

    print(f"[Temporal Anomaly Detector] NTP UTC:   {ntp_utc.isoformat(timespec='microseconds')}")
    print(f"[Temporal Anomaly Detector] Time difference: {time_diff:.2f} seconds (threshold: {args.threshold:.2f}s).")

    if time_diff > args.threshold:
        print("[Temporal Anomaly Detector] Status: WARNING! Temporal Anomaly Detected! Your system clock is significantly out of sync.", file=sys.stderr)
        sys.exit(1)
    else:
        print("[Temporal Anomaly Detector] Status: All clear. No temporal anomalies detected.")
        sys.exit(0)

if __name__ == '__main__':
    main()
