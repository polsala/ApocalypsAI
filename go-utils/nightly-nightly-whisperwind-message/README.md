# Nightly Whisperwind Message Relay

A whimsical-yet-useful Go-based concurrent HTTP service that acts as a "Whisperwind Message Relay." It receives incoming JSON POST messages and concurrently fans them out to multiple configured target endpoints, reporting on the delivery status for each.

This utility is perfect for scenarios where you need to broadcast an event or message to several downstream services without blocking the initial sender, and you want to know which "listening posts" successfully received the "whisper."

## Features

*   **Concurrent Relaying**: Messages are forwarded to all configured targets simultaneously using Go's goroutines.
*   **Configurable Targets**: Target URLs are specified via an environment variable, making deployment flexible.
*   **Detailed Status Reports**: Provides a JSON response indicating the success or failure for each target endpoint, including error messages if applicable.
*   **Simple HTTP API**: Exposes a single `/relay` endpoint for receiving messages.

## Usage

### 1. Build the Utility

Navigate to the `src` directory and build the Go application:

```bash
cd src
go build -o whisperwind-relay .
```

### 2. Configure Target Endpoints

Set the `TARGET_URLS` environment variable with a comma-separated list of the HTTP/S endpoints where messages should be relayed.

Example:
```bash
export TARGET_URLS="http://localhost:8081/listener1,https://api.example.com/webhook,http://192.168.1.100:8080/event"
```

You can also set the `PORT` environment variable to change the listening port (default is `8080`).

```bash
export PORT=9000
```

### 3. Run the Relay Service

```bash
./whisperwind-relay
```

The service will start listening on the configured port (default 8080) at the `/relay` path.

### 4. Send Messages to the Relay

Send a `POST` request with a JSON body to the `/relay` endpoint. The `message` field in the request body should contain the JSON payload you wish to relay.

**Example Request (using `curl`):**

```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"message": {"event_type": "apocalypse_imminent", "severity": "critical", "details": "Temporal anomaly detected near sector 7G."}}' \
     http://localhost:8080/relay
```

**Example Response:**

```json
{
  "results": [
    {
      "url": "http://localhost:8081/listener1",
      "status": "success"
    },
    {
      "url": "https://api.example.com/webhook",
      "status": "failed",
      "error": "Target responded with status 500: {\"error\":\"internal server error\"}"
    },
    {
      "url": "http://192.168.1.100:8080/event",
      "status": "success"
    }
  ]
}
```

If `TARGET_URLS` is not set, the relay will report a "skipped" status:

```json
{
  "results": [
    {
      "url": "N/A",
      "status": "skipped",
      "error": "No target URLs configured"
    }
  ]
}
```

## Development

### Running Tests

Navigate to the `src` directory and run the Go tests:

```bash
cd src
go test -v .
```

The tests use `httptest.NewServer` to mock target endpoints, ensuring they are deterministic and do not rely on external network access.
