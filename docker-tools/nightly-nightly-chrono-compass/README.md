# Nightly Chrono-Compass

A containerized utility designed to help the community maintain accurate timekeeping in a world where reliable time sources might be scarce or corrupted. The Chrono-Compass periodically queries multiple Network Time Protocol (NTP) servers, calculates the average time, and reports any significant drift in the local system's clock. Think of it as your personal temporal anchor, ensuring you're always on schedule for the next supply drop or anomaly detection.

## Features

*   **Multi-NTP Source Verification**: Queries a configurable list of NTP servers for robust time synchronization.
*   **Drift Reporting**: Clearly indicates the offset between local system time and the "true" average NTP time.
*   **Containerized**: Easy to deploy and run in any Docker-compatible environment.
*   **Configurable Interval**: Adjust how frequently the time checks occur.

## Usage

### Prerequisites

*   Docker installed and running.

### Running with Docker Compose

1.  Save the `docker-compose.yml` file in a directory.
2.  (Optional) Create a `.env` file in the same directory to override default NTP servers or interval:
    ```
    NTP_SERVERS="pool.ntp.org,time.google.com"
    CHECK_INTERVAL_SECONDS=300 # Check every 5 minutes
    ```
3.  Run the service:
    ```bash
    docker-compose up -d
    ```
4.  View logs to see time drift reports:
    ```bash
    docker-compose logs -f chrono-compass
    ```

### Running Manually (Docker)

1.  Build the Docker image:
    ```bash
    docker build -t chrono-compass .
    ```
2.  Run the container, specifying NTP servers and interval (optional):
    ```bash
    docker run -d --name chrono-compass \
      -e NTP_SERVERS="pool.ntp.org,time.google.com" \
      -e CHECK_INTERVAL_SECONDS=60 \
      chrono-compass
    ```
3.  View logs:
    ```bash
    docker logs -f chrono-compass
    ```

### Configuration

The following environment variables can be set:

*   `NTP_SERVERS`: Comma-separated list of NTP server hostnames (default: `pool.ntp.org,time.google.com,time.nist.gov`).
*   `CHECK_INTERVAL_SECONDS`: How often (in seconds) to perform the time check (default: `300`).

## Example Output

```
[2023-10-27 10:30:00] Chrono-Compass initiating temporal scan...
[2023-10-27 10:30:01] NTP Server: pool.ntp.org, Offset: -0.001234s
[2023-10-27 10:30:01] NTP Server: time.google.com, Offset: 0.000567s
[2023-10-27 10:30:01] NTP Server: time.nist.gov, Offset: -0.000100s
[2023-10-27 10:30:01] Average NTP Offset: -0.000256s
[2023-10-27 10:30:01] Local System Time: 2023-10-27 10:30:01.123456
[2023-10-27 10:30:01] Adjusted NTP Time:   2023-10-27 10:30:01.123712
[2023-10-27 10:30:01] Local clock drift detected: ahead of average NTP by 0.000256 seconds.
[2023-10-27 10:30:01] Next scan in 300 seconds.
```
