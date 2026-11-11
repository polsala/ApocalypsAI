# Nightly Temporal Drift Stabilizer

A Dockerized utility designed to combat temporal inconsistencies within containerized environments. In the chaotic aftermath, ensuring your applications' clocks are synchronized is paramount for reliable logging, transaction processing, and data integrity. This tool periodically synchronizes a container's system clock with a specified NTP server.

## Features

*   **Automated Time Sync:** Continuously adjusts the container's clock to prevent drift.
*   **Configurable:** Easily set the NTP server and synchronization interval via environment variables.
*   **Lightweight:** Built on Alpine Linux with `ntpdate` for minimal overhead.

## How it Works

The `nightly-temporal-drift-stabilizer` runs as a long-lived process within a Docker container. it uses `ntpdate` to query an NTP server (defaulting to `pool.ntp.org`) and adjust the container's system clock. This process repeats at a configurable interval.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-temporal-drift-stabilizer` directory and build the image:

```bash
docker build -t nightly-temporal-drift-stabilizer .
```

### 2. Run the Container

You can run the container directly, specifying your desired NTP server and synchronization interval:

```bash
docker run -d \
  --name my-stabilizer \
  -e NTP_SERVER="time.google.com" \
  -e SYNC_INTERVAL=60 \
  --cap-add=SYS_TIME \
  nightly-temporal-drift-stabilizer
```

**Note:** The `--cap-add=SYS_TIME` flag is crucial as it grants the container the necessary permissions to modify the system clock. Without it, `ntpdate` will fail.

#### Environment Variables:

*   `NTP_SERVER`: (Optional) The NTP server to synchronize with. Defaults to `pool.ntp.org`.
*   `SYNC_INTERVAL`: (Optional) The interval in seconds between synchronization attempts. Defaults to `300` (5 minutes).

### 3. Verify Synchronization

Check the container logs to see the synchronization attempts and results:

```bash
docker logs my-stabilizer
```

## Development and Testing

See the `tests/` directory for how to run automated tests and verify the utility's functionality.
