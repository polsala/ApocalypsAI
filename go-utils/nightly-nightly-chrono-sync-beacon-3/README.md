# Nightly Chrono-Sync Beacon

The `nightly-chrono-sync-beacon` is a whimsical yet crucial Go-based utility designed to provide a reliable, local time synchronization service for the ApocalypsAI community's distributed tools and agents. In an environment where external time sources might be erratic or unavailable, this beacon ensures that all connected components can maintain a consistent and shared understanding of "now."

It operates as a simple TCP server, listening for "SYNC" requests and responding with the current UTC timestamp. This allows various agents to align their internal clocks, coordinate actions, and log events with temporal precision.

## Features

*   **Local Time Synchronization**: Provides a consistent UTC timestamp to connected clients.
*   **Lightweight & Concurrent**: Built with Go, leveraging goroutines for efficient handling of multiple client connections.
*   **Simple TCP Protocol**: Easy to integrate with any language or tool capable of making TCP connections.

## How to Run

1.  **Build the executable**:
    ```bash
    cd go-utils/nightly-chrono-sync-beacon/src
    go build -o chrono-sync-beacon main.go
    ```
2.  **Run the server**:
    ```bash
    ./chrono-sync-beacon --port 8080
    ```
    (Default port is 8080 if not specified)

## How to Use (Client Example)

You can connect to the beacon using `netcat` or a simple client script in any language.

**Using `netcat` (for testing/manual sync):**

```bash
echo "SYNC" | nc localhost 8080
```

The server will respond with a UTC timestamp string, e.g.: `2023-10-27T10:30:00.123456789Z\n`

**Example Go Client:**

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
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		fmt.Println("Error connecting:", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Fprintf(conn, "SYNC\n")
	message, _ := bufio.NewReader(conn).ReadString('\n')
	fmt.Print("Received synchronized time: " + message)

	// Parse and use the time
	t, err := time.Parse(time.RFC3339Nano, message[:len(message)-1]) // Remove newline
	if err != nil {
		fmt.Println("Error parsing time:", err)
		os.Exit(1)
	}
	fmt.Println("Parsed time:", t)
}
```

## Automated Tests

To run the tests, navigate to the utility's root directory and execute:

```bash
cd go-utils/nightly-chrono-sync-beacon
go test ./...
```

The tests simulate client connections and verify the server's responses without requiring actual network interfaces for internal logic, ensuring determinism and offline execution. Tests involving actual network binding use ephemeral ports and timeouts to remain robust.
