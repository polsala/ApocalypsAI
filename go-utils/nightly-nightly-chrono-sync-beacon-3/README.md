# Nightly Chrono-Sync Beacon

## Overview

The `nightly-chrono-sync-beacon` is a whimsical-yet-critical utility designed to provide a reliable, synchronized time source for distributed systems operating in potentially unstable or "temporally distorted" environments. It functions as a simple TCP server that broadcasts highly accurate UTC timestamps to all connected clients at a configurable interval. This allows client applications to synchronize their internal clocks, coordinate events, or simply maintain a consistent sense of time.

## Features

*   **Concurrent Client Handling**: Efficiently manages multiple client connections using Go's goroutines.
*   **Configurable Broadcast Interval**: Adjust how frequently time signals are sent.
*   **JSON Output**: Time signals are sent as easy-to-parse JSON objects.
*   **Graceful Shutdown**: Designed to shut down cleanly when signaled.

## Usage

### Running the Server

To start the Chrono-Sync Beacon server, you can build and run the `main.go` file. The server listens on a specified port and broadcasts time signals at a given interval.

```bash
# Build the executable
go build -o chrono-sync-beacon src/main.go

# Run the server (default port 8080, interval 1 second)
./chrono-sync-beacon

# Or specify port and interval via environment variables
PORT=8081 INTERVAL_SECONDS=5 ./chrono-sync-beacon
```

**Environment Variables:**

*   `PORT`: The TCP port the server will listen on (default: `8080`).
*   `INTERVAL_SECONDS`: The interval in seconds between sending time signals (default: `1`).

### Connecting a Client

Clients can connect to the beacon server using a simple TCP connection and read JSON messages. Here's a minimal Go client example:

```go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"time"
)

// BeaconMessage matches the server's output structure
type BeaconMessage struct {
	Timestamp string `json:"timestamp"`
	Source    string `json:"source"`
}

func main() {
	serverAddr := "localhost:8080" // Adjust if your server is on a different host/port
	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		log.Fatalf("Failed to connect to beacon server: %v", err)
	}
	defer conn.Close()

	log.Printf("Connected to Chrono-Sync Beacon at %s", serverAddr)

	decoder := json.NewDecoder(conn)
	for {
		var msg BeaconMessage
		if err := decoder.Decode(&msg); err != nil {
			log.Printf("Error decoding message or server disconnected: %v", err)
			return
		}
		fmt.Printf("Received time signal from %s: %s\n", msg.Source, msg.Timestamp)
		// Here you would use msg.Timestamp to synchronize your application
	}
}
```

## Development

### Running Tests

The utility includes automated tests to ensure its functionality and robustness. To run the tests:

```bash
go test ./tests/...
```

Tests will start a temporary server on an ephemeral port, connect clients, and verify that time signals are received correctly and in the expected format. Logs from the server during tests are suppressed for cleaner output.
