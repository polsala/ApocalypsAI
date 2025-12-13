# Nightly Chrono-Sync Beacon

A whimsical-yet-useful Go-based network service that acts as a temporal beacon for distributed apocalyptic outposts. It broadcasts and serves a synchronized "apocalyptic" time, allowing for configurable temporal offsets to simulate various spacetime anomalies or just to keep things interesting.

## Features

*   **Configurable Temporal Offset**: Adjust the time reported by the beacon by a specified number of seconds (positive or negative).
*   **Unique Beacon ID**: Identify your beacon in a network of temporal anomalies.
*   **Simple HTTP API**: Query the current adjusted time via a straightforward `/time` endpoint.
*   **Concurrency**: Built with Go's concurrency model for efficient handling of multiple time synchronization requests.

## Usage

### Prerequisites

*   Go (version 1.16 or higher)

### Running the Beacon Server

1.  **Navigate to the utility directory:**
    ```bash
    cd go-utils/nightly-chrono-sync-beacon
    ```

2.  **Run the server:**
    ```bash
    go run src/main.go --port 8080 --offset 3600 --id "APOCALYPSAI-ALPHA-BEACON"
    ```
    *   `--port`: (Optional) The port the server will listen on (default: `8080`).
    *   `--offset`: (Optional) The temporal offset in seconds to apply to UTC time. Can be positive (future) or negative (past). Default: `0`.
    *   `--id`: (Optional) A unique identifier for this beacon. Default: `APOCALYPSAI-BEACON-001`.

    The server will start and log its configuration.

### Querying the Beacon

Once the server is running, you can query it using `curl` or any HTTP client:

```bash
curl http://localhost:8080/time
```

Example response:

```json
{
  "beacon_id": "APOCALYPSAI-ALPHA-BEACON",
  "current_time_utc": "2023-10-27T10:00:00.123456789Z",
  "temporal_offset_seconds": 3600,
  "message": "Time synchronized from the ApocalypsAI Chrono-Sync Beacon. May your chronometers be ever true (or whimsically skewed)."
}
```
*(Note: `current_time_utc` will reflect the actual UTC time plus the specified `temporal_offset_seconds`.)*

## Development

### Running Tests

To ensure the beacon is functioning correctly and its temporal integrity is maintained, run the automated tests:

```bash
cd go-utils/nightly-chrono-sync-beacon
go test tests/test_main.go src/main.go -v
```

The tests use `httptest` to simulate HTTP requests and responses, ensuring deterministic and offline validation of the beacon's logic.
