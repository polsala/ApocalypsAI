# Nightly Void Whisper Relay

## Summary

The `nightly-void-whisper-relay` is a whimsical-yet-useful Go TCP server designed to relay messages, or 'void whispers', between multiple connected clients. Each message passed through the relay undergoes a minor, deterministic 'distortion' before being broadcast to all other active clients. It's a simple, concurrent network tool perfect for demonstrating basic Go networking, goroutines, and channels, or for a fun, slightly-off-kilter chat experience.

## Features

*   **Concurrent Client Handling**: Manages multiple client connections simultaneously using Go's goroutines.
*   **Message Broadcasting**: Relays messages from any client to all other connected clients.
*   **Whimsical Distortion**: Applies a simple, deterministic transformation to each message (appending `~void echo~`) before broadcasting.
*   **Self-Contained**: Built entirely with Go's standard library.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-void-whisper-relay
    ```

2.  **Build the server executable**:
    ```bash
    go build -o void-whisper-relay src/main.go
    ```

3.  **Start the server**:
    ```bash
    ./void-whisper-relay
    ```
    The server will start listening on `localhost:8080`.

## How to Connect Clients

You can use `netcat` (nc) or write a simple client in any language to connect to the relay.

### Using `netcat` (nc)

Open multiple terminal windows and run:

```bash
# Terminal 1 (Client A)
nc localhost 8080
```

```bash
# Terminal 2 (Client B)
nc localhost 8080
```

Now, type messages in one terminal and press Enter. You will see the message (with its distortion) appear in the other connected terminals.

**Example Interaction:**

*   **Client A types**: `Hello from the void!`
*   **Client B sees**: `Hello from the void! ~void echo~`
*   **Client B types**: `Whispers received.`
*   **Client A sees**: `Whispers received. ~void echo~`

## Development & Testing

To run the automated tests:

```bash
cd go-utils/nightly-void-whisper-relay
go test ./tests
```

The tests will start a server instance, connect multiple simulated clients, send messages, and verify that the messages are received correctly with the expected distortion.
