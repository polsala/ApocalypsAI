import datetime
import requests
import json
import sys
import argparse

DEFAULT_EXTERNAL_TIME_URL = "http://worldtimeapi.org/api/ip"

def get_local_time():
    """Returns the current local system time as a datetime object."""
    return datetime.datetime.now()

def get_external_time(url: str) -> datetime.datetime | None:
    """Fetches the current time from an external API and returns it as a datetime object.

    Args:
        url: The URL of the external time API.

    Returns:
        A datetime object representing the external time, or None if fetching fails.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        # WorldTimeAPI returns 'datetime' in ISO 8601 format
        # Example: '2023-10-27T10:30:00.123456+00:00'
        # We need to parse it and remove timezone info for simple comparison
        dt_str = data.get('datetime')
        if dt_str:
            # Parse ISO 8601 string, then convert to naive datetime
            # Use fromisoformat for Python 3.7+
            dt_obj = datetime.datetime.fromisoformat(dt_str)
            return dt_obj.replace(tzinfo=None) # Remove timezone for naive comparison
        else:
            print(f"[ERROR] 'datetime' key not found in external API response from {url}", file=sys.stderr)
            return None
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request to {url} timed out after 5 seconds.", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch external time from {url}: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to decode JSON from external API response from {url}", file=sys.stderr)
        return None
    except ValueError as e:
        print(f"[ERROR] Failed to parse datetime string from external API response from {url}: {e}", file=sys.stderr)
        return None

def calculate_drift(local_time: datetime.datetime, external_time: datetime.datetime) -> float:
    """Calculates the time drift in seconds between local and external times."""
    return (local_time - external_time).total_seconds()

def report_drift(drift_seconds: float):
    """Prints a human-readable report of the time drift."""
    abs_drift = abs(drift_seconds)
    status = "aligned" if abs_drift < 0.1 else ("ahead" if drift_seconds > 0 else "behind")
    level = "INFO" if abs_drift < 1.0 else "WARNING"

    if abs_drift < 0.1:
        print(f"[{level}] System time is closely aligned with external source (drift: {drift_seconds:.6f} seconds).")
    else:
        print(f"[{level}] Significant time drift detected: {drift_seconds:.6f} seconds (local is {status}).")

def main():
    parser = argparse.ArgumentParser(description="Check and report system time drift against an external source.")
    parser.add_argument('--url', type=str, default=DEFAULT_EXTERNAL_TIME_URL,
                        help=f"URL of the external time API (default: {DEFAULT_EXTERNAL_TIME_URL})")
    args = parser.parse_args()

    print(f"[INFO] Starting Temporal Rift Time-Sync check...")

    local_time = get_local_time()
    print(f"[INFO] Local time: {local_time}")

    external_time = get_external_time(args.url)
    if external_time is None:
        print("[ERROR] Could not retrieve external time. Aborting drift check.", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] External time: {external_time}")

    drift = calculate_drift(local_time, external_time)
    report_drift(drift)

    if abs(drift) >= 1.0: # Exit with error if drift is 1 second or more
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
