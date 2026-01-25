# nightly-beacon-whisperer

A Go-based utility for broadcasting and receiving short, encrypted "whispers" (messages) over a local network, acting as a distributed, low-bandwidth communication beacon for survivors.

## Description

In the desolate quiet of the post-apocalypse, communication is a lifeline. The `nightly-beacon-whisperer` provides a simple, robust way to send and receive short, vital messages across a local network. Whether you're broadcasting a "All clear" signal or listening for distant calls for aid, this utility leverages Go's concurrency to keep the whispers flowing. Messages are lightly "encrypted" using a whimsical XOR cipher, ensuring your vital tidbits remain just that – whispers.

## Features

*   **Beacon Mode**: Periodically broadcasts a configurable message to the local network.
*   **Listener Mode**: Continuously listens for and displays incoming beacon messages.
*   **Whimsical Encryption**: Simple XOR cipher for message obfuscation.
*   **Lightweight & Concurrent**: Built with Go for efficient network operations.

## Usage

First, build the utility:

```bash
go build -o beacon-whisperer src/main.go
```

### Beacon Mode

To start a beacon that broadcasts a message every 5 seconds:

```bash
./beacon-whisperer --mode beacon --id "Sector-7 Outpost" --msg "Supplies low. Seeking trade." --port 8080 --interval 10s
```

*   `--mode beacon`: Specifies beacon operation.
*   `--id <sender_id>`: Your unique identifier (e.g., "Sector-7 Outpost").
*   `--msg <message>`: The message to broadcast (e.g., "All clear. Hope endures.").
*   `--port <port_number>`: The UDP port to use (default: 8080).
*   `--interval <duration>`: How often to broadcast (e.g., `5s`, `1m`).

### Listener Mode

To start a listener that awaits whispers on a specific port:

```bash
./beacon-whisperer --mode listen --port 8080
```

*   `--mode listen`: Specifies listener operation.
*   `--port <port_number>`: The UDP port to listen on (must match beacon's port).

### Example Interaction

Run a listener in one terminal:
```bash
./beacon-whisperer --mode listen --port 8080
```
Expected output (after a beacon starts):
```
2023/10/27 10:30:00 Listener active on UDP port 8080, awaiting whispers...
Received whisper from Sector-7 Outpost (192.168.1.100:8080): "Supplies low. Seeking trade." (at 2023-10-27T10:30:05Z)
Received whisper from Another-Beacon (192.168.1.101:8080): "Water source found near old bridge." (at 2023-10-27T10:30:10Z)
```

Run a beacon in another terminal:
```bash
./beacon-whisperer --mode beacon --id "My-Shelter" --msg "All clear. Hope endures." --port 8080 --interval 5s
```
Expected output:
```
2023/10/27 10:30:00 Beacon 'My-Shelter' listening on UDP port 8080 and broadcasting every 5s...
2023/10/27 10:30:05 Broadcasted whisper: "All clear. Hope endures."
Received whisper from Sector-7 Outpost (192.168.1.100:8080): "Supplies low. Seeking trade." (at 2023-10-27T10:30:05Z)
2023/10/27 10:30:10 Broadcasted whisper: "All clear. Hope endures."
```

## Development

### Building

```bash
go build -o beacon-whisperer src/main.go
```

### Running Tests

```bash
go test ./tests/...
```
