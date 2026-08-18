# Nightly Chrono-Sync Beacon

## Overview

The `nightly-chrono-sync-beacon` is a whimsical-yet-useful Go-based utility designed to help maintain temporal harmony across your distributed systems. In the chaotic post-apocalyptic landscape, time can be a fickle mistress. This tool acts as a digital sundial and chronometer, broadcasting precise time signals (beacons) and listening for them to detect any temporal drift or anomalies between your nodes.

It operates in two modes:

1.  **Emitter**: Periodically broadcasts the local system's precise Unix nanosecond timestamp over UDP to a specified address and port.
2.  **Listener**: Listens for these beacons, compares the received timestamp with its own local time, and reports the observed time difference (drift).

This helps identify which systems are lagging, leading, or simply out of sync, ensuring your distributed operations remain perfectly choreographed.

## Features

*   **Lightweight**: Built with Go for minimal resource consumption.
*   **Concurrent**: Utilizes Go's goroutines for efficient beacon emission and listening.
*   **UDP-based**: Fast, connectionless communication suitable for broadcasting.
*   **Drift Detection**: Clearly reports temporal discrepancies.
*   **Configurable**: Easily set broadcast intervals, ports, and multicast/broadcast addresses.

## Installation

To build the utility, ensure you have Go (1.16 or newer) installed.

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-chrono-sync-beacon/src
go build -o ../nightly-chrono-sync-beacon .
```

The executable `nightly-chrono-sync-beacon` will be created in the parent directory.

## Usage

### Emitter Mode

To start broadcasting time beacons:

```bash
./nightly-chrono-sync-beacon emit \
  -id "Chronos-Node-Alpha" \
  -port 8080 \
  -interval 1s \
  -address "239.0.0.1" # Use a multicast address or broadcast address (e.g., 192.168.1.255)
```

**Arguments:**

*   `-id <string>`: A unique identifier for this beacon emitter (e.g., "Server-1", "Gateway-A"). (Required)
*   `-port <int>`: The UDP port to send beacons on. (Default: `8080`)
*   `-interval <duration>`: How often to send a beacon (e.g., `500ms`, `1s`, `10s`). (Default: `1s`)
*   `-address <string>`: The IP address to send beacons to. Can be a unicast, broadcast (e.g., `192.168.1.255`), or multicast address (e.g., `239.0.0.1`). (Default: `127.0.0.1`)

### Listener Mode

To start listening for time beacons and report drift:

```bash
./nightly-chrono-sync-beacon listen \
  -port 8080 \
  -address "239.0.0.1" # Must match the emitter's address if using multicast
```

**Arguments:**

*   `-port <int>`: The UDP port to listen on. (Default: `8080`)
*   `-address <string>`: The IP address to listen on. If using multicast, this should be the multicast group address. If listening on a specific interface for broadcast, use `0.0.0.0`. (Default: `0.0.0.0`)

**Output (Listener Mode):**

```
[2023-10-27 10:30:05.123456789] Received beacon from Chronos-Node-Alpha (192.168.1.100:8080). Drift: +123.456µs
[2023-10-27 10:30:06.123456789] Received beacon from Chronos-Node-Beta (192.168.1.101:8080). Drift: -78.901µs
```

*   A positive drift means the emitter's clock is ahead of the listener's clock.
*   A negative drift means the emitter's clock is behind the listener's clock.

## Example Scenario

1.  **Node A (Emitter)**:
    ```bash
    ./nightly-chrono-sync-beacon emit -id "Main-Server" -port 8080 -interval 500ms -address "239.0.0.1"
    ```
2.  **Node B (Listener)**:
    ```bash
    ./nightly-chrono-sync-beacon listen -port 8080 -address "239.0.0.1"
    ```
3.  **Node C (Listener)**:
    ```bash
    ./nightly-chrono-sync-beacon listen -port 8080 -address "239.0.0.1"
    ```

Node B and C will continuously report the temporal drift relative to Node A, helping you identify and correct any time synchronization issues.

## Contributing

Feel free to contribute to the temporal stability of the ApocalypsAI community! Submit issues or pull requests to enhance the Chrono-Sync Beacon's capabilities.
