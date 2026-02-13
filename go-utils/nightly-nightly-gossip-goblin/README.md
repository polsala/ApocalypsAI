# Nightly Gossip Goblin

A lightweight, concurrent Go service that implements a simple gossip protocol. Nodes (Goblins) can send and receive ephemeral messages, propagating them through a network. Useful for distributed status updates, light coordination, or just spreading digital whispers.

## Features

*   **Ephemeral Messaging**: Share short, transient messages.
*   **Distributed Gossip**: Messages propagate through configured peers.
*   **Concurrent**: Handles multiple incoming and outgoing messages efficiently using Go goroutines.
*   **CLI Interface**: Easily start a goblin server or send a message to a running goblin.

## Usage

### Prerequisites

*   Go 1.16+ installed

### Build

```bash
go build -o gossip-goblin src/main.go
```

### Start a Gossip Goblin Server

To start a goblin server that listens on a specific port and knows about other peers:

```bash
./gossip-goblin server --port 8080 --peers "http://localhost:8081,http://localhost:8082"
```

*   `--port`: The port the goblin server will listen on (e.g., `8080`).
*   `--peers`: A comma-separated list of URLs of other goblin servers to gossip messages to (e.g., `"http://localhost:8081,http://localhost:8082"`). This is optional; a goblin can start without knowing any peers initially.

### Send a Message to a Gossip Goblin

To send a message to a running goblin server:

```bash
./gossip-goblin send --target "http://localhost:8080" --message "Beware the temporal rifts!"
```

*   `--target`: The URL of the goblin server to send the message to (e.g., `"http://localhost:8080"`).
*   `--message`: The content of the gossip message.

### Example Workflow

1.  **Start Goblin A:**
    ```bash
    ./gossip-goblin server --port 8080 --peers "http://localhost:8081"
    ```

2.  **Start Goblin B:**
    ```bash
    ./gossip-goblin server --port 8081 --peers "http://localhost:8080"
    ```

3.  **Send a message to Goblin A:**
    ```bash
    ./gossip-goblin send --target "http://localhost:8080" --message "The moon is made of cheese!"
    ```

    You should see Goblin A log the message, and then Goblin B will also log the message as it's gossiped.

## Development

### Run Tests

```bash
go test ./tests/...
```

## Configuration

*   **Server Port**: Configured via `--port` argument.
*   **Known Peers**: Configured via `--peers` argument (comma-separated URLs).
*   **Gossip Timeout**: Hardcoded to 5 seconds for peer communication.

## License

This utility is released under the MIT License. See the main repository for details.
