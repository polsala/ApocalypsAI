# Nightly Stardust Streamer

The `nightly-stardust-streamer` is a whimsical yet robust Go-based utility designed to simulate a post-apocalyptic data collection service. It acts as a concurrent TCP server, listening for incoming "stardust particles" (simple text messages) from various sources. Each particle is processed, timestamped, and logged, demonstrating a basic, resilient event streaming mechanism.

This utility is perfect for:
*   Learning Go's concurrency features (`goroutines`, `channels`, `sync.WaitGroup`).
*   Understanding basic TCP server implementation.
*   Prototyping simple event collection systems.
*   Adding a touch of cosmic charm to your data pipelines.

## Features

*   **Concurrent Handling**: Processes multiple incoming connections simultaneously using goroutines.
*   **Simple Protocol**: Accepts plain text lines as "stardust particles".
*   **Timestamping**: Each received particle is automatically timestamped.
*   **Graceful Shutdown**: Handles `SIGINT` and `SIGTERM` signals to shut down cleanly, waiting for active connections to finish.

## Installation

1.  **Ensure Go is installed**: You need Go 1.16 or newer.
    ```bash
    go version
    ```
2.  **Clone the repository**: If you haven't already, clone the ApocalypsAI repository.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-stardust-streamer
    ```
3.  **Build the executable**: Navigate to the utility's directory and build.
    ```bash
    go build -o stardust-streamer src/main.go
    ```

## Usage

### Running the Server

You You can run the server on the default port (8080) or specify a custom port using the `PORT` environment variable.

```bash
# Run on default port 8080
./stardust-streamer

# Run on a custom port, e.g., 9000
PORT=9000 ./stardust-streamer
```

The server will log processed messages to standard output.

### Sending Stardust Particles (Client Example)

You can use `netcat` (nc) or a simple Go client to send messages to the streamer.

**Using `netcat`:**

```bash
# Connect to the server (assuming it's running on localhost:8080)
nc localhost 8080

# Type your stardust particles, each on a new line, then press Enter.
# Press Ctrl+D to close the connection.
# Example:
# First cosmic dust
# A faint signal from sector 7
# Anomaly detected
```

**Using a simple Go client (example `client.go`):**

```go
package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"time"
)

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	address := fmt.Sprintf("localhost:%s", port)

	conn, err := net.Dial("tcp", address)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to connect to %s: %v\n", address, err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Printf("Connected to Stardust Streamer at %s. Type messages and press Enter. Ctrl+D to exit.\n", address)
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		message := scanner.Text()
		_, err := fmt.Fprintf(conn, "%s\n", message)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Failed to send message: %v\n", err)
			break
		}
		time.Sleep(50 * time.Millisecond) // Small delay to prevent overwhelming the server
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "Error reading stdin: %v\n", err)
	}
	fmt.Println("Client disconnected.")
}
```
To run the client:
```bash
# Save the above content as client.go in a separate directory
go run client.go
```

## Development

### Running Tests

To run the automated tests for the `nightly-stardust-streamer`:

```bash
cd go-utils/nightly-stardust-streamer/tests
go test -v
```

The tests use a mock network connection (`mockNetConn`) to ensure they are deterministic and do not rely on actual network ports, making them suitable for offline execution.
