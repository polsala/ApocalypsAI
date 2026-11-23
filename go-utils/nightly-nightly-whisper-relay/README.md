# Nightly Whisper Relay (nightly-whisper-relay)

A concurrent Go service designed to relay messages between connected clients, simulating a distributed 'whispering wind' communication network across the ApocalypsAI wasteland.

## Purpose

In a world of intermittent signals and fragmented communication, the Nightly Whisper Relay acts as a simple, robust message hub. Clients connect to the relay, send text messages, and these messages are then broadcast to all *other* currently connected clients. It's a low-latency, text-based communication channel, perfect for sharing quick updates, warnings, or even just a friendly 'hello' across the digital ether.

## Features

*   **Concurrent Handling**: Efficiently manages multiple client connections using Go's goroutines.
*   **Broadcast Messaging**: Any message sent by one client is relayed to all other active clients.
*   **Simple Protocol**: Uses newline-delimited text messages over TCP, making it easy to interact with using standard network tools.
*   **Lightweight**: Minimal resource footprint, ideal for deployment in resource-constrained environments.

## How to Run

1.  **Build the executable:**
    ```bash
    cd nightly-whisper-relay/src
    go build -o ../bin/whisper-relay .
    ```
2.  **Run the server:**
    ```bash
    ./bin/whisper-relay -port 8080
    ```
    (Replace `8080` with your desired port. If no port is specified, it defaults to `8080`.)

## How to Use (Client Examples)

You can connect to the relay using `netcat` (nc) or a simple Go client.

### Using `netcat` (nc)

Open multiple terminal windows and connect to the server:

**Terminal 1 (Client A):**
```bash
nc localhost 8080
```

**Terminal 2 (Client B):**
```bash
nc localhost 8080
```

Now, type messages in one terminal and press Enter. You will see the messages appear in the *other* terminal(s).

Example interaction:

**Client A (typing):**
```
Hello from Client A!
```

**Client B (receives):**
```
Hello from Client A!
```

**Client B (typing):**
```
Client B hears you!
```

**Client A (receives):**
```
Client B hears you!
```

### Using a Simple Go Client

Create a file `client.go`:

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
		return
	}
	defer conn.Close()

	fmt.Println("Connected to Whisper Relay. Type messages and press Enter.")

	go func() {
		scanner := bufio.NewScanner(conn)
		for scanner.Scan() {
			fmt.Printf("\rReceived: %s\n> ", scanner.Text())
		}
		if err := scanner.Err(); err != nil {
			fmt.Println("Error reading from connection:", err)
		}
		fmt.Println("Server disconnected.")
		os.Exit(0)
	}()

	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("> ")
		text, _ := reader.ReadString('\n')
		_, err := fmt.Fprintf(conn, text)
		if err != nil {
			fmt.Println("Error writing to connection:", err)
			return
		}
		time.Sleep(10 * time.Millisecond) // Small delay to prevent busy loop
	}
}
```

Run this client in multiple terminals:

```bash
go run client.go
```

Messages typed in one client will appear in the others.
