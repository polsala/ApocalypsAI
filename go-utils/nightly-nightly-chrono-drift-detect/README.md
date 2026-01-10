# Nightly Chrono-Drift Detector

## Overview

The `nightly-chrono-drift-detect` is a whimsical-yet-useful Go-based TCP server designed to help identify clock synchronization issues across distributed systems. Clients connect to the server, send their local Unix nanosecond timestamp, and the server responds with the calculated clock drift, along with a configurable simulated network latency.

This utility is perfect for:
*   **Testing time synchronization**: Verify if your distributed services are keeping accurate time relative to a central authority.
*   **Simulating network conditions**: Understand how network latency affects perceived clock drift.
*   **Debugging distributed systems**: Pinpoint which nodes might be experiencing significant clock skew.

## Features
*   Simple TCP server.
*   Accepts Unix nanosecond timestamps from clients.
*   Calculates the difference between client time and server time at the moment of receipt.
*   Applies a configurable simulated network latency before responding.
*   Outputs client time, server time (pre- and post-latency), calculated clock drift, and simulated latency.

## How to Build

1.  **Navigate to the utility directory:**
    ```bash
    cd go-utils/nightly-chrono-drift-detect
    ```
2.  **Build the Go executable:**
    ```bash
    go build -o chrono-drift-detector src/main.go
    ```

## How to Run

1.  **Start the server:**
    ```bash
    ./chrono-drift-detector
    ```
    The server will listen on `localhost:8080` by default with a simulated latency of 100ms.

    You can customize the port and simulated latency using environment variables:
    ```bash
    PORT=8081 SIMULATED_LATENCY_MS=250 ./chrono-drift-detector
    ```

## How to Use

Clients can connect via `netcat` or a simple program and send their current Unix nanosecond timestamp followed by a newline.

### Example Client (using `netcat`)

1.  **Get current Unix nanoseconds (e.g., in Bash):**
    ```bash
    CURRENT_NANO=$(date +%s%N)
    echo $CURRENT_NANO
    ```

2.  **Send to the server and receive response:**
    ```bash
    echo $CURRENT_NANO | nc localhost 8080
    ```

    **Expected Output:**
    ```
    OK: Client Time: 2023-10-27T10:30:00.123456789Z, Server Time (pre-latency): 2023-10-27T10:30:00.123460000Z, Server Time (post-latency): 2023-10-27T10:30:00.223460000Z, Clock Drift: -3.211µs, Simulated Latency: 100ms
    ```
    *   `Client Time`: The timestamp sent by the client.
    *   `Server Time (pre-latency)`: The server's time when it received the client's message.
    *   `Server Time (post-latency)`: The server's time after applying the simulated latency.
    *   `Clock Drift`: `Client Time - Server Time (pre-latency)`. A positive value means the client's clock is ahead of the server's.
    *   `Simulated Latency`: The configured delay applied by the server.

### Example Client (Go program)

```go
package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"time"
)

func main() {
	conn, err := net.Dial("tcp", "localhost:8080")
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer conn.Close()

	clientTime := time.Now().UnixNano()
	fmt.Fprintf(conn, "%d\n", clientTime)

	response, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		log.Fatalf("Failed to read response: %v", err)
	}

	fmt.Print("Server Response: ", response)
}
```

## Configuration

The server can be configured via environment variables:

*   `PORT`: The port the server will listen on (default: `8080`).
*   `SIMULATED_LATENCY_MS`: The simulated network latency in milliseconds (default: `100`).
