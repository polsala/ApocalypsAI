# Nightly WhisperNet Relay

A robust and whimsical Go service designed to relay critical messages across the fragmented communication channels of the post-apocalyptic world. It ensures your whispers reach their intended recipients, even when the network is as unpredictable as a mutated squirrel.

The WhisperNet Relay listens for incoming HTTP POST requests, buffers the message, and then concurrently attempts to deliver it to a configurable list of target URLs. It features built-in retry logic with exponential backoff to brave the most intermittent connections.

## Features

*   **Concurrent Delivery**: Sends messages to multiple targets simultaneously using Go goroutines.
*   **Reliable Retries**: Configurable retry attempts and delay with exponential backoff for resilient delivery.
*   **Simple HTTP API**: Easy to integrate with any system capable of sending HTTP POST requests.
*   **Lightweight**: Built with Go for minimal resource consumption.

## Usage

### 1. Build and Run

```bash
# Clone the repository (or navigate to this utility's directory)
# cd go-utils/nightly-whispernet-relay

# Build the executable
go build -o whispernet-relay src/main.go

# Run the service (configure targets via environment variables)
TARGET_URLS="http://localhost:8081/listener,http://localhost:8082/listener" RETRY_ATTEMPTS=5 RETRY_DELAY_SECONDS=1 ./whispernet-relay
```

### 2. Configuration

The WhisperNet Relay is configured via environment variables:

*   `PORT`: The port the relay service will listen on (default: `8080`).
*   `TARGET_URLS`: A comma-separated list of URLs where messages should be relayed. **Required.**
    Example: `http://listener1.example.com/receive,http://listener2.example.com/receive`
*   `RETRY_ATTEMPTS`: The maximum number of times to retry sending a message to a target (default: `3`).
*   `RETRY_DELAY_SECONDS`: The initial delay in seconds before retrying (default: `1`). This delay will double with each subsequent retry (exponential backoff).

### 3. Sending Messages to the Relay

Send an HTTP POST request to the relay's `/relay` endpoint. The body of the request will be the message content.

```bash
curl -X POST -H "Content-Type: text/plain" \
     -d "Urgent: Supplies low at Sector 7. Requesting immediate resupply." \
     http://localhost:8080/relay
```

The relay will respond with `200 OK` if it successfully received the message and initiated the relay process. It does not wait for all targets to confirm receipt.

### 4. Status Endpoint

A simple `/status` endpoint is available to check if the relay is running.

```bash
curl http://localhost:8080/status
```

Expected output: `WhisperNet Relay is operational.`

## Development

### Running Tests

```bash
go test ./tests/...
```

## Example Scenario

Imagine you have a remote sensor outpost that occasionally sends critical alerts. These alerts need to reach multiple command centers, but the network connection to these centers is highly unstable.

1.  Deploy `nightly-whispernet-relay` on a stable intermediary server.
2.  Configure `TARGET_URLS` to point to the HTTP endpoints of your command centers.
3.  The sensor outpost sends its alerts to the `nightly-whispernet-relay`'s `/relay` endpoint.
4.  The relay takes care of retrying delivery to each command center until successful (or retry limit is reached), ensuring maximum message propagation.
