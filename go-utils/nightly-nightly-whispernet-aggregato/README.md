# Nightly WhisperNet Aggregator (Go)

The `nightly-whispernet-aggregator` is a whimsical-yet-useful Go service designed to capture ephemeral "whispers" from the network, aggregate them over a short period, and then distill them into a "collective thought" that is logged or broadcast. Think of it as a digital ear for the ambient chatter of your distributed systems, turning fleeting messages into periodic insights.

## Features

*   **Ephemeral Message Capture**: Listens for lightweight UDP messages (whispers).
*   **Concurrent Handling**: Utilizes Go's goroutines to efficiently process multiple incoming whispers.
*   **Time-Based Aggregation**: Collects whispers over a configurable interval.
*   **Collective Thought Generation**: Summarizes the collected whispers into a single output.
*   **Simple Logging**: Outputs the collective thought to standard output.

## Why use it?

*   **Lightweight Telemetry**: Send fire-and-forget metrics or status updates without the overhead of persistent connections.
*   **Distributed Gossip**: Allow various microservices or agents to "chat" without a central message queue.
*   **Ambient System Awareness**: Get a periodic pulse of what's happening across your infrastructure.
*   **Whimsical Fun**: Because sometimes, your systems just need to whisper their secrets.

## How to Run

1.  **Build the service:**
    ```bash
    go build -o whispernet-aggregator src/main.go
    ```

2.  **Run the service:**
    ```bash
    ./whispernet-aggregator -port 8080 -interval 5s
    ```
    *   `-port`: The UDP port to listen on (default: `8080`).
    *   `-interval`: The duration to aggregate whispers before forming a collective thought (e.g., `5s`, `10s`, `1m`) (default: `10s`).

## How to Send Whispers

You can send whispers using `netcat` or a simple Go client.

**Using `netcat` (Linux/macOS):**
```bash
echo "Hello from client A" | nc -u -w 1 127.0.0.1 8080
echo "System status: OK" | nc -u -w 1 127.0.0.1 8080
echo "Initiating phase shift" | nc -u -w 1 127.0.0.1 8080
```
*   `-u`: UDP mode
*   `-w 1`: Timeout for sending (important for UDP)

**Using a simple Go client (example `send_whisper.go`):**
```go
package main

import (
	"fmt"
	"net"
	"os"
	"time"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: go run send_whisper.go <message> <port>")
		os.Exit(1)
	}
	message := os.Args[1]
	port := os.Args[2]
	serverAddr, err := net.ResolveUDPAddr("udp", "127.0.0.1:"+port)
	if err != nil {
		fmt.Printf("Error resolving address: %v\n", err)
		os.Exit(1)
	}

	conn, err := net.DialUDP("udp", nil, serverAddr)
	if err != nil {
		fmt.Printf("Error dialing UDP: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	_, err = conn.Write([]byte(message))
	if err != nil {
		fmt.Printf("Error sending message: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Sent whisper: \"%s\" to port %s\n", message, port)
	time.Sleep(100 * time.Millisecond) // Give time for message to be sent
}
```
Run it: `go run send_whisper.go "Another secret" 8080`

## Development

To run tests:
```bash
go test ./tests/...
```
