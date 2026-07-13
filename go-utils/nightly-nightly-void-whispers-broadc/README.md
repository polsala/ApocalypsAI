# Nightly Void Whispers Broadcast

## Summary

The `nightly-void-whispers-broadcast` is a whimsical-yet-useful Go-based server designed to broadcast ephemeral, one-way "whispers" to multiple connected clients. It simulates a low-latency, non-persistent communication channel, perfect for quick status updates, event notifications, or simply sending fleeting messages across a distributed network without the overhead of a full message queue.

Think of it as a digital megaphone for the void, where messages are heard by all who listen, but never linger.

## Features

*   **Concurrent Client Handling**: Efficiently manages multiple client connections using Go's goroutines.
*   **One-Way Broadcast**: Messages sent to the server are immediately fanned out to all active listeners.
*   **Ephemeral**: Messages are not stored or persisted; they are broadcast and then gone.
*   **Simple TCP Protocol**: Clients connect via a standard TCP socket and receive newline-delimited messages.
*   **Self-Contained**: A single Go binary for the server, with a simple client example.

## How to Use

### 1. Build the Server and Client

Navigate to the `src` directory and build the Go binaries:

```bash
cd go-utils/nightly-void-whispers-broadcast/src
go build -o void-whispers-server server.go
go build -o void-whispers-client client_example.go
```

### 2. Run the Server

Start the server on a desired port (e.g., `8080`):

```bash
./void-whispers-server
```

The server will output:
`Void Whispers Broadcast Server listening on port 8080...`

### 3. Connect Clients

Open one or more new terminal windows and run the client, specifying the server address and port:

```bash
./void-whispers-client localhost:8080
```

Each client will output:
`Connected to Void Whispers Broadcast Server at localhost:8080. Listening for whispers...`

### 4. Send Whispers (from the server's perspective)

Currently, the `server.go` example runs indefinitely. To send messages, you would integrate the `Broadcast` method into another application or modify `main` function of `server.go` to accept input or trigger broadcasts. For demonstration, you can modify `server.go`'s `main` function temporarily:

```go
// Inside server.go's main function, after go server.Start("8080")

// Example: Broadcast a message every 3 seconds
// go func() {
// 	for i := 0; ; i++ {
// 		message := fmt.Sprintf("Whisper %d from the void at %s", i, time.Now().Format(time.RFC3339))
// 		server.Broadcast(message)
// 		log.Printf("Sent: %s", message)
// 		time.Sleep(3 * time.Second)
// 	}
// }()

// Or, to send a single message after a delay:
// time.AfterFunc(5 * time.Second, func() {
// 	server.Broadcast("A single, profound whisper.")
// })

// Block forever, or until Ctrl+C
fmt.Println("Server running. Press Ctrl+C to stop.")
select {} // Block forever
```

After modifying and rebuilding `server.go`, run it again. Your connected clients will start receiving the broadcasted messages.

## Development

### Project Structure

```
nightly-void-whispers-broadcast/
├── README.md
├── src/
│   ├── server.go          # The main broadcast server logic
│   └── client_example.go  # A simple client to demonstrate connection and message reception
└── tests/
    └── server_test.go     # Unit and integration tests for the server
```

### Running Tests

Navigate to the `tests` directory and run the Go tests:

```bash
cd go-utils/nightly-void-whispers-broadcast/tests
go test -v
```

Tests use `localhost` network connections to simulate client-server interactions in a deterministic and offline manner. They verify client connection, message broadcasting, client disconnection handling, and server shutdown.

## Use Cases

*   **Apocalyptic Alert System**: Broadcast urgent, short-lived warnings to all connected survivor outposts.
*   **Distributed Health Checks**: Send periodic "heartbeat" whispers from a central monitor to various services.
*   **Event Notification**: Notify all interested parties about a transient event (e.g., "Resource cache found at Sector 7!").
*   **Game State Updates**: Push real-time, non-critical game state changes to multiple clients in a simple game.
*   **Ephemeral Chat**: A very basic, non-persistent chat system where messages are only seen by current listeners.
