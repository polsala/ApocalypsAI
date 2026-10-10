import ntplib
import time
import os
from datetime import datetime, timedelta

def get_ntp_time_offset(ntp_server):
    """
    Queries a single NTP server and returns the offset between local time and server time.
    Returns None if the query fails.
    """
    try:
        client = ntplib.NTPClient()
        response = client.request(ntp_server, version=3)
        # response.offset is (local_receive_time - server_transmit_time)
        return response.offset
    except ntplib.NTPException as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Failed to query NTP server {ntp_server}: {e}")
        return None
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] UNEXPECTED ERROR with {ntp_server}: {e}")
        return None

def main():
    ntp_servers_str = os.getenv("NTP_SERVERS", "pool.ntp.org,time.google.com,time.nist.gov")
    ntp_servers = [s.strip() for s in ntp_servers_str.split(',') if s.strip()]
    check_interval_seconds = int(os.getenv("CHECK_INTERVAL_SECONDS", "300"))

    if not ntp_servers:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: No NTP servers configured. Exiting.")
        return

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Chrono-Compass initialized with servers: {', '.join(ntp_servers)}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking every {check_interval_seconds} seconds.")

    while True:
        current_local_time = datetime.now()
        print(f"\n[{current_local_time.strftime('%Y-%m-%d %H:%M:%S')}] Chrono-Compass initiating temporal scan...")

        offsets = []
        for server in ntp_servers:
            offset = get_ntp_time_offset(server)
            if offset is not None:
                offsets.append(offset)
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NTP Server: {server}, Offset: {offset:.6f}s")

        if not offsets:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] WARNING: No successful NTP server responses. Cannot determine average offset.")
        else:
            average_offset = sum(offsets) / len(offsets)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Average NTP Offset: {average_offset:.6f}s")

            # The average_offset is (local_time - server_time).
            # If offset is positive, local time is ahead of server time.
            # If offset is negative, local time is behind server time.
            
            # To get the "true" NTP time, we subtract the offset from local time.
            adjusted_ntp_time = current_local_time - timedelta(seconds=average_offset)

            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Local System Time: {current_local_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Adjusted NTP Time:   {adjusted_ntp_time.strftime('%Y-%m-%d %H:%M:%S.%f')}")
            
            # Report drift relative to local system time
            # If average_offset is positive, local is ahead. If negative, local is behind.
            drift_direction = "ahead of" if average_offset > 0 else "behind"
            drift_value = abs(average_offset)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Local clock drift detected: {drift_direction} average NTP by {drift_value:.6f} seconds.")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Next scan in {check_interval_seconds} seconds.")
        time.sleep(check_interval_seconds)

if __name__ == "__main__":
    main()
