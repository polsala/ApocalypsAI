# Nightly WhisperNet Hub

## Summary
`nightly-whisper-net-hub` is a Go-based concurrent HTTP server designed to collect and aggregate 'whispers' (small, structured messages) from various distributed network nodes. It simulates a resilient communication hub in a fragmented, post-apocalyptic environment, where faint signals need to be gathered and understood.

## Features
- **Concurrent Message Collection**: Handles multiple incoming 'whisper' POST requests simultaneously using Go's goroutines.
- **Message Aggregation**: Stores whispers grouped by their 'origin' node.
- **Status Endpoint**: Provides a JSON overview of all collected whispers.
- **Lightweight**: Built with Go's standard library for minimal dependencies and efficient performance.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-whisper-net-hub
    ```

2.  **Run the server**:
    ```bash
    go run src/main.go
    ```
    The server will start listening on `http://localhost:8080`.

## How to Use

### 1. Send a Whisper
Send a POST request to the `/whisper` endpoint with a JSON body containing `origin` and `message` fields.

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"origin": "node-alpha", "message": "The winds whisper of change..."}' \
     http://localhost:8080/whisper

curl -X POST -H "Content-Type: application/json" \
     -d '{"origin": "node-beta", "message": "Found a shiny bottlecap near the old bridge."}' \
     http://localhost:8080/whisper

curl -X POST -H "Content-Type: application/json" \
     -d '{"origin": "node-alpha", "message": "Supply cache coordinates updated: 34.0522, -118.2437"}' \
     http://localhost:8080/whisper
```

### 2. Check Status
Send a GET request to the `/status` endpoint to retrieve all collected whispers, grouped by origin.

**Example using `curl`:**

```bash
curl http://localhost:8080/status | jq .
```

**Expected Output (example):**
```json
{
  "node-alpha": [
    {
      "origin": "node-alpha",
      "message": "The winds whisper of change...",
      "timestamp": "2023-10-27T10:00:00Z"
    },
    {
      "origin": "node-alpha",
      "message": "Supply cache coordinates updated: 34.0522, -118.2437",
      "timestamp": "2023-10-27T10:01:30Z"
    }
  ],
  "node-beta": [
    {
      "origin": "node-beta",
      "message": "Found a shiny bottlecap near the old bridge.",
      "timestamp": "2023-10-27T10:00:45Z"
    }
  ]
}
```

## Automated Tests

To run the tests for the WhisperNet Hub:

```bash
cd go-utils/nightly-whisper-net-hub
go test ./tests/...
```

The tests cover basic whisper handling, status retrieval, and concurrent message processing, ensuring the hub operates reliably.
