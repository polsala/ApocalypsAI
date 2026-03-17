# Nightly Chronal Beacon

## Purpose

The `nightly-chronal-beacon` is a whimsical-yet-useful Go-based utility designed to help distributed systems maintain a sense of "temporal awareness" within a network. It acts as a persistent, low-overhead temporal signal, broadcasting its unique "chronal signature" (a timestamp and a unique identifier) to a specified UDP multicast address at regular intervals.

While playfully named, this beacon can serve practical purposes:

*   **Service Discovery**: Nodes can listen for beacons to discover active participants in a network segment without a central registry.
*   **Temporal Drift Detection**: By comparing the beacon's timestamp with their own local clock, listening nodes can detect and potentially compensate for temporal drift.
*   **Network Reachability**: The consistent broadcast acts as a heartbeat, indicating network health and reachability to the beacon's host.
*   **Distributed Synchronization**: Provides a common, albeit unauthenticated, time reference for loosely coupled systems.

## How it Works

The beacon operates by:

1.  Initializing a UDP connection to a specified multicast address and port.
2.  Periodically (e.g., every 5 seconds) constructing a JSON message containing its unique ID and the current UTC timestamp.
3.  Broadcasting this "chronal signature" message to the multicast group.
4.  Running indefinitely until stopped.

## Usage

### Build

To build the beacon executable:

```bash
go build -o chronal-beacon src/main.go
```

### Run the Beacon

```bash
./chronal-beacon \
  --id "TemporalNode-Alpha" \
  --interval 5s \
  --port 9999 \
  --multicast-addr "224.0.0.1"
```

**Parameters:**

*   `--id`: A unique identifier for this beacon instance (e.g., "Server-1", "Sensor-Gamma"). Defaults to a random UUID.
*   `--interval`: The frequency at which the beacon broadcasts its signature (e.g., `1s`, `500ms`). Defaults to `5s`.
*   `--port`: The UDP port to use for multicast. Defaults to `9999`.
*   `--multicast-addr`: The multicast IP address to broadcast to. Defaults to `224.0.0.1`.

### Listen for Beacons (Example using `netcat` or a simple Go listener)

To observe the beacon's broadcasts, you can use `netcat` (if your system supports UDP multicast listening):

```bash
netcat -ul 9999
```

Or, you can write a simple Go program to listen for multicast messages (as demonstrated in the `tests/beacon_test.go` file).

**Example Output (JSON format):**

```json
{"id":"TemporalNode-Alpha","timestamp":"2023-10-27T10:30:05.123456789Z"}
```

## Development

### Prerequisites

*   Go 1.16+ installed

### Running Tests

```bash
go test ./tests/...
```
