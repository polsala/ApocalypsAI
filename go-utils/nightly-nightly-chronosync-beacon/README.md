# Nightly Chronosync Beacon

A Go-based network service designed to broadcast synchronized 'temporal pulses' (timestamps) to connected clients. In the chaotic post-apocalyptic timeline, maintaining accurate time synchronization is crucial for coordinating efforts and understanding temporal anomalies. This beacon provides a reliable source of UTC timestamps via HTTP and WebSocket.

## Features

*   **HTTP Pulse Endpoint (`/pulse`)**: Provides the current UTC timestamp in RFC3339Nano format upon request.
*   **WebSocket Stream Endpoint (`/stream`)**: Continuously broadcasts UTC timestamps at a 1-second interval to all connected WebSocket clients.
*   **Concurrent Design**: Leverages Go's goroutines and channels to efficiently handle multiple client connections.
*   **Graceful Shutdown**: Handles `SIGINT` and `SIGTERM` signals for a clean shutdown.

## Getting Started

### Prerequisites

*   Go (version 1.16 or higher)

### Installation

1.  Clone the repository (or navigate to this utility's directory):

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chronosync-beacon
    ```

2.  The utility is self-contained. No external Go modules are strictly required beyond standard library and `golang.org/x/net/websocket` (which will be fetched automatically by `go mod tidy`).

### Running the Beacon

To start the Chronosync Beacon server:

```bash
cd src
go run main.go
```

The beacon will start on `http://localhost:8080` by default. You can specify a different port using the `PORT` environment variable:

```bash
PORT=8081 go run src/main.go
```

### Usage

#### 1. HTTP Pulse Endpoint

Access the `/pulse` endpoint using `curl` or your web browser:

```bash
curl http://localhost:8080/pulse
# Expected output:
# Temporal Pulse: 2023-10-27T10:30:00.123456789Z
```

#### 2. WebSocket Stream Endpoint

Connect to the `/stream` endpoint using a WebSocket client. Here's an example using `wscat` (install with `npm install -g wscat`):

```bash
wscat -c ws://localhost:8080/stream
# Expected output (timestamps will stream every second):
# < 2023-10-27T10:30:01.123456789Z
# < 2023-10-27T10:30:02.123456789Z
# < 2023-10-27T10:30:03.123456789Z
# ...
```

## Testing

To run the automated tests for the Chronosync Beacon:

```bash
cd tests
go test -v .
```

The tests will verify both the HTTP `/pulse` endpoint and the WebSocket `/stream` functionality, ensuring the beacon operates as expected.
