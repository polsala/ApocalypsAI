# Nightly Temporal Echo Listener

A Go-based concurrent service designed to capture and aggregate 'temporal echoes' – simulated network pings or messages originating from various time-displaced nodes across the multiverse. It provides a simple HTTP API to receive these echoes and retrieve a real-time summary of all captured temporal events.

## Whimsical Purpose

In the ever-shifting sands of the apocalypse, understanding the whispers from the past and the murmurs of potential futures can be crucial. The Temporal Echo Listener acts as a central nexus, patiently awaiting any stray data packets that manage to pierce the temporal veil. Whether it's a warning from a forgotten timeline or a casual greeting from a future self, this utility ensures no echo goes unheard.

## Practical Usefulness

While whimsical in theme, this utility demonstrates a practical pattern for building a simple, concurrent HTTP service in Go:

-   **Message Aggregation**: Collects data from multiple sources into a central store.
-   **Concurrent Handling**: Efficiently handles multiple incoming requests using Go's goroutines.
-   **API Endpoint**: Provides a clear API for data submission and retrieval.
-   **State Management**: Manages in-memory state safely with mutexes.

This can be adapted for real-world scenarios like log aggregation, simple event collection, or as a lightweight message queue for internal services.

## How to Run

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.
2.  **Navigate**: Change into the `nightly-temporal-echo-listener` directory.
3.  **Run**: Execute the main application:
    ```bash
    go run src/main.go
    ```
    The service will start on `http://localhost:8080`.

## How to Use

### 1. Send a Temporal Echo (POST /echo)

Send a JSON payload to the `/echo` endpoint to register a new temporal echo. The `timestamp` field will be automatically set by the server upon receipt.

**Endpoint**: `POST http://localhost:8080/echo`
**Content-Type**: `application/json`

**Example Request (using curl)**:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"source": "Past-Node-7", "message": "Did anyone see my temporal wrench?"}' \
     http://localhost:8080/echo

curl -X POST -H "Content-Type: application/json" \
     -d '{"source": "Future-Outpost-Alpha", "message": "Beware the paradox squirrels!"}' \
     http://localhost:8080/echo
```

### 2. Get Temporal Echo Summary (GET /summary)

Retrieve a JSON array of all collected temporal echoes.

**Endpoint**: `GET http://localhost:8080/summary`
**Content-Type**: `application/json`

**Example Request (using curl)**:
```bash
curl http://localhost:8080/summary
```

**Example Response**:
```json
[
  {
    "source": "Past-Node-7",
    "message": "Did anyone see my temporal wrench?",
    "timestamp": "2023-10-27T10:30:00.123456789Z"
  },
  {
    "source": "Future-Outpost-Alpha",
    "message": "Beware the paradox squirrels!",
    "timestamp": "2023-10-27T10:30:05.987654321Z"
  }
]
```

## Development

### Running Tests

To run the automated tests, navigate to the utility's root directory and execute:

```bash
go test ./tests/...
```

Tests are designed to be deterministic and run offline using Go's `net/http/httptest` package to simulate HTTP requests and responses without requiring a live server.
