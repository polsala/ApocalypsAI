# Nightly Chronosync Beacon

A whimsical-yet-useful Go-based network utility for synchronizing time across disparate systems in a post-apocalyptic network. The Chronosync Beacon acts as a reliable, local time source, allowing clients to query it via UDP and adjust their internal clocks to a consistent "beacon time."

## Features

*   **UDP-based Time Synchronization**: Lightweight and efficient communication.
*   **Concurrent Server**: Handles multiple client requests simultaneously using Go's goroutines.
*   **Simple Client**: Queries the beacon and displays the synchronized time.
*   **Resilient Design**: Designed for environments where external NTP sources might be unavailable or unreliable.

## How it Works

The `chronosync-beacon` server listens on a specified UDP port. Upon receiving any UDP packet, it responds with its current Unix nanosecond timestamp. Clients send a request to the beacon, receive the timestamp, and can then calculate their time offset, adjusting for network latency.

## Installation

1.  **Prerequisites**: Ensure Go (version 1.16 or higher) is installed on your system.
2.  **Clone the repository**: If you haven't already, clone the ApocalypsAI repository.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chronosync-beacon
    ```
3.  **Build the server and client**: Navigate to the utility's directory and build the executables.
    ```bash
    go mod tidy
    go build -o bin/chronosync-beacon-server ./src/server
    go build -o bin/chronosync-beacon-client ./src/client
    ```

## Usage

### Running the Chronosync Beacon Server

The server will listen on UDP port `8080` by default. You can specify a different port using the `-port` flag.

```bash
./bin/chronosync-beacon-server -port 8080
```

Example output:
```
Chronosync Beacon Server listening on UDP :8080
```

### Using the Chronosync Beacon Client

The client will query the beacon server at `localhost:8080` by default. You can specify a different server address using the `-server` flag.

```bash
./bin/chronosync-beacon-client -server localhost:8080
```

Example output:
```
Querying Chronosync Beacon at localhost:8080...
Beacon Time (UTC): 2023-10-27T10:30:45.123456789Z (Unix Nano: 1698393045123456789)
```

## Development and Testing

To run the tests:

```bash
go test ./tests
```
