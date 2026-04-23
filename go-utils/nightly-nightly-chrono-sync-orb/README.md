# Nightly Chrono-Sync Orb

The Nightly Chrono-Sync Orb is a whimsical Go-based utility designed to broadcast slightly-offset current UTC time pulses over a local UDP multicast network. It's perfect for systems that need a "generally correct" time source with a touch of cosmic unpredictability, or just for fun distributed time-keeping experiments.

## Features

*   **UDP Multicast Broadcast:** Sends time pulses to a configurable multicast address and port.
*   **Whimsical Time Offset:** Each pulse includes a small, random positive or negative offset (up to 5 seconds) to simulate minor temporal distortions.
*   **Configurable Interval:** Adjust how frequently the Orb broadcasts its time.
*   **Lightweight Go Implementation:** Efficient and easy to deploy.

## Usage

### Running the Orb (Server)

1.  **Build:**
    ```bash
    go build -o chrono-sync-orb src/main.go
    ```
2.  **Run:**
    ```bash
    ./chrono-sync-orb
    ```
    The Orb will start broadcasting on `224.0.0.1:9000` by default, every 3 seconds.

### Configuration

You can configure the multicast address, port, and broadcast interval using environment variables:

*   `ORB_MULTICAST_ADDR`: Multicast IP address (default: `224.0.0.1`)
*   `ORB_PORT`: UDP port (default: `9000`)
*   `ORB_INTERVAL_SECONDS`: Broadcast interval in seconds (default: `3`)
*   `ORB_MAX_OFFSET_SECONDS`: Maximum whimsical offset in seconds (default: `5`)

Example:
```bash
ORB_MULTICAST_ADDR="239.0.0.1" ORB_PORT="9001" ORB_INTERVAL_SECONDS="1" ./chrono-sync-orb
```

### Listening to the Orb (Client Example)

You can use `netcat` or a simple Go program to listen for the Orb's pulses.

**Using `netcat` (Linux/macOS):**
```bash
# For multicast, you might need to specify the interface, e.g., -i eth0
# This example assumes your system is configured for multicast listening on the default interface.
nc -ul 224.0.0.1 9000
```
*Note: `netcat` might not handle multicast subscriptions directly on all systems. A dedicated client is more reliable.*

**Simple Go Client:**

Create a file `client.go` in the same directory as `chrono-sync-orb` (or anywhere you like):
```go
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
	"time"
)

type TimePulse struct {
	Timestamp string `json:"timestamp"`
	OffsetSec float64 `json:"offset_sec"`
	Message   string `json:"message"`
}

func main() {
	multicastAddr := os.Getenv("ORB_MULTICAST_ADDR")
	if multicastAddr == "" {
		multicastAddr = "224.0.0.1"
	}
	port := os.Getenv("ORB_PORT")
	if port == "" {
		port = "9000"
	}

	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%s", multicastAddr, port))
	if err != nil {
		log.Fatalf("Error resolving UDP address: %v", err)
	}

	conn, err := net.ListenMulticastUDP("udp", nil, addr)
	if err != nil {
		log.Fatalf("Error listening to multicast UDP: %v", err)
	}
	defer conn.Close()

	log.Printf("Listening for Chrono-Sync Orb pulses on %s:%s...", multicastAddr, port)

	buffer := make([]byte, 1024)
	for {
		n, src, err := conn.ReadFromUDP(buffer)
		if err != nil {
			log.Printf("Error reading from UDP: %v", err)
			continue
		}

		var pulse TimePulse
		if err := json.Unmarshal(buffer[:n], &pulse); err != nil {
			log.Printf("Error unmarshalling JSON from %s: %v", src, err)
			continue
		}

		parsedTime, err := time.Parse(time.RFC3339Nano, pulse.Timestamp)
		if err != nil {
			log.Printf("Error parsing timestamp from %s: %v", src, err)
			continue
		}

		fmt.Printf("Received pulse from %s: %s (Offset: %.2fs) - \"%s\"\n",
			src, parsedTime.Local().Format(time.RFC3339), pulse.OffsetSec, pulse.Message)
	}
}
```
To run the client:
```bash
go run client.go
```

## Development

### Running Tests

```bash
go test ./...
```
