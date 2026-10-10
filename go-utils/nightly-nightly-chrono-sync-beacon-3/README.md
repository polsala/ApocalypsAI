# Nightly Chrono-Sync Beacon

## Overview

The `nightly-chrono-sync-beacon` is a whimsical-yet-useful Go utility designed to establish temporal consistency in a world where traditional time synchronization services might be unreliable. It consists of two main components:

1.  **Beacon Server**: A lightweight UDP server that periodically broadcasts the current UTC time with nanosecond precision to a specified network address (defaulting to localhost).
2.  **Chrono-Sync Client**: A UDP client that listens for these beacon signals, parses the received time, and calculates the drift between its local system clock and the beacon's synchronized time.

This utility is ideal for scenarios requiring local, high-precision time synchronization without relying on external NTP servers, such as coordinating distributed systems, scientific experiments in isolated environments, or simply ensuring all your post-apocalyptic gadgets are on the same temporal page.

## Features

*   **High Precision**: Broadcasts time in RFC3339Nano format for nanosecond accuracy.
*   **Lightweight**: Built with Go's efficient concurrency model for minimal resource usage.
*   **Configurable**: Port, broadcast interval, and target address can be configured via environment variables.
*   **Local Synchronization**: Provides a self-contained time source for local networks.

## Usage

### Prerequisites

*   Go (version 1.16 or higher)

### Building

Navigate to the utility's root directory and build both the beacon server and the client:

```bash
cd go-utils/nightly-chrono-sync-beacon
go build -o bin/beacon src/beacon/main.go
go build -o bin/client src/client/main.go
```

This will create `beacon` and `client` executables in the `bin/` directory.

### Running the Beacon Server

The beacon server will broadcast the current UTC time. By default, it sends to `127.0.0.1:8080` every 1 second.

```bash
./bin/beacon
# Or with custom settings:
BEACON_PORT=8081 BEACON_INTERVAL_SECONDS=5 BEACON_TARGET_ADDR=192.168.1.255 ./bin/beacon
```

**Environment Variables:**

*   `BEACON_PORT`: The UDP port to use for broadcasting (default: `8080`).
*   `BEACON_INTERVAL_SECONDS`: The interval in seconds between broadcasts (default: `1`).
*   `BEACON_TARGET_ADDR`: The IP address to send the beacon to (default: `127.0.0.1`). For network-wide broadcast, use your subnet's broadcast address (e.g., `192.168.1.255`).

### Running the Chrono-Sync Client

The client will listen for beacon signals and display the received time along with its local drift.

```bash
./bin/client
# Or with a custom port:
BEACON_PORT=8081 ./bin/client
```

**Environment Variables:**

*   `BEACON_PORT`: The UDP port to listen on (default: `8080`). This must match the `BEACON_PORT` used by the server.

## Example Output

**Beacon Server:**

```
Chrono-Sync Beacon broadcasting to 127.0.0.1:8080 every 1s...
Broadcasted: 2023-10-27T10:30:00.123456789Z
Broadcasted: 2023-10-27T10:30:01.234567890Z
...
```

**Chrono-Sync Client:**

```
Chrono-Sync Client listening for beacons on UDP port 8080...
Received: 2023-10-27T10:30:00.123456789Z (Local Drift: 12.345µs)
Received: 2023-10-27T10:30:01.234567890Z (Local Drift: -5.678µs)
...
```

## Development

### Running Tests

To run the automated tests for both the beacon and client components:

```bash
cd go-utils/nightly-chrono-sync-beacon
go test ./tests/beacon_test.go
go test ./tests/client_test.go
```

Tests are designed to be deterministic and run offline using mocks for network interactions and time-sensitive operations.
