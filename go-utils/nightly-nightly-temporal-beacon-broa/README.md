# Nightly Temporal Beacon Broadcaster

## Summary

The `nightly-temporal-beacon-broadcaster` is a whimsical-yet-useful Go utility designed to simulate broadcasting messages across various 'temporal relays'. It demonstrates concurrent network requests, error handling, and structured output in Go. Each relay responds with a status, an optional message, and a 'temporal distortion' metric, giving you insight into the fabric of spacetime (or at least, your network).

## Usage

To run the broadcaster, provide your message as the first argument, followed by one or more URLs of your temporal relays. These relays are expected to be HTTP POST endpoints that accept a JSON payload `{"message": "Your message"}` and respond with `{"status": "received", "temporal_distortion": 0.5, "relay_message": "Echo from the past!"}`.

```bash
go run src/main.go "Greetings from the present!" http://localhost:8081/broadcast http://localhost:8082/broadcast
```

**Example Output:**

```
Broadcasting message "Greetings from the present!" to 2 temporal relays...

--- Broadcast Results ---
  [SUCCESS] Relay: http://localhost:8081/broadcast, Distortion: 0.75, Message: "Echo from temporal node at 2024-07-20T12:34:56Z: \"Greetings from the present!\""
  [FAILURE] Relay: http://localhost:8082/broadcast, Error: Relay responded with status 500: {"error": "Temporal anomaly detected"}
```

### Building the Executable

You can build a standalone executable:

```bash
go build -o nightly-temporal-beacon-broadcaster src/main.go
./nightly-temporal-beacon-broadcaster "Hello future!" http://localhost:8080/broadcast
```

## Development and Testing

### Running Tests

The utility includes automated tests that use mock HTTP clients to ensure deterministic and offline validation of the broadcasting logic.

```bash
go test ./tests/...
```

### Mock Temporal Relay Server (for local development)

While not part of this utility's core code, you might want a simple mock server to test against locally. Here's a conceptual Go snippet for a basic relay server:

```go
// Save this as `mock_relay_server.go` and run it in a separate terminal:
// go run mock_relay_server.go

package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"net/http"
	"time"
)

// BroadcastRequest represents the payload sent to a temporal relay.
type BroadcastRequest struct {
	Message string `json:"message"`
}

// BroadcastResponse represents the response received from a temporal relay.
type BroadcastResponse struct {
	Status           string  `json:"status"`
	TemporalDistortion float64 `json:"temporal_distortion"`
	RelayMessage     string  `json:"relay_message,omitempty"`
	Error            string  `json:"error,omitempty"`
}

func main() {
	rand.Seed(time.Now().UnixNano())

	http.HandleFunc("/broadcast", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
			return
		}

		var req BroadcastRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid request body", http.StatusBadRequest)
			return
		}

		// Simulate some processing time
		time.Sleep(time.Duration(rand.Intn(100)+50) * time.Millisecond)

		// Simulate temporal distortion
		distortion := rand.Float64() * 10.0 // 0.0 to 10.0

		// Simulate occasional failure
		if rand.Intn(10) == 0 { // 10% chance of failure
			http.Error(w, `{"error": "Temporal anomaly detected"}`, http.StatusInternalServerError)
			return
		}

		resp := BroadcastResponse{
			Status:           "received",
			TemporalDistortion: distortion,
			RelayMessage:     fmt.Sprintf("Echo from temporal node at %s: \"%s\"", time.Now().Format(time.RFC3339), req.Message),
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(resp)
	})

	port := 8081 // You can change this port
	fmt.Printf("Mock Temporal Relay Server listening on :%d\n", port)
	http.ListenAndServe(fmt.Sprintf(":%d", port), nil)
}
```
