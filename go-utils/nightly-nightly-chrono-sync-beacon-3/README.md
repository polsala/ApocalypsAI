# Nightly Chrono-Sync Beacon

A Go-based peer-to-peer utility for broadcasting and receiving ephemeral status beacons across a network. This tool allows nodes to emit periodic 'heartbeat' messages with custom payloads, and other nodes to listen for these messages, providing a simple, distributed way to share status or presence information.

## Features

*   **Beacon Mode**: Broadcasts a configurable message at a specified interval.
*   **Listen Mode**: Receives and displays beacons from other nodes.
*   **Lightweight**: Uses UDP for efficient, low-overhead communication.
*   **Concurrent**: Leverages Go's goroutines for efficient sending and receiving.

## Usage

### Build

To build the utility, navigate to the `src` directory and run:

```bash
go build -o chrono-sync-beacon
```

### Run in Beacon Mode (Sender)

To start a beacon sender, specify a unique ID, the target address (multicast or unicast UDP), the message payload, and the broadcast interval.

```bash
./chrono-sync-beacon beacon \
  --id "AlphaBase-01" \
  --addr "224.0.0.1:9000" \
  --payload "Status: Operational" \
  --interval "5s"
```

*   `--id`: A unique identifier for this beacon sender (e.g., "Server-A", "Sensor-Hub-Gamma").
*   `--addr`: The UDP address to send beacons to (e.g., `127.0.0.1:9000` for local, `224.0.0.1:9000` for multicast).
*   `--payload`: The message content to include in the beacon.
*   `--interval`: How often to send the beacon (e.g., `1s`, `10s`, `1m`).

### Run in Listen Mode (Receiver)

To start a beacon listener, specify the address to listen on. This should typically match the address used by the senders.

```bash
./chrono-sync-beacon listen \
  --addr "224.0.0.1:9000"
```

*   `--addr`: The UDP address to listen on. For multicast, ensure your system is configured to join the multicast group.

## Example Workflow

1.  Start a listener on one terminal:
    ```bash
    ./chrono-sync-beacon listen --addr "127.0.0.1:9000"
    ```
2.  Start a sender on another terminal:
    ```bash
    ./chrono-sync-beacon beacon --id "Node-X" --addr "127.0.0.1:9000" --payload "Online" --interval "2s"
    ```
3.  You should see "Node-X: Online" messages appearing in the listener terminal every 2 seconds.

## Configuration

All configuration is done via command-line flags. Refer to the `Usage` section for details.

## Development

### Testing

To run the tests, navigate to the `src` directory and run:

```bash
go test ./...
```

Tests are designed to be deterministic and offline, using Go's `net` package for in-memory network simulation where necessary, or focusing on message serialization/deserialization logic.
