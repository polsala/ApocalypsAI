# nightly-chronal-sync-beacon

The `nightly-chronal-sync-beacon` is a whimsical Go-based network utility designed to provide a time synchronization service, with a twist. It can serve the current time, or intentionally introduce "temporal drift" and "anomalies" to simulate various time-related challenges in distributed systems.

## Purpose

In the post-apocalyptic landscape, reliable timekeeping is crucial, but sometimes you need to test how your systems react to *unreliable* time. This beacon allows you to:
- Provide a standard time source.
- Simulate network latency or clock drift by adding a configurable offset.
- Inject sudden, short-lived "temporal anomalies" to test system resilience.

## Usage

### Running the Beacon

To run the beacon server:

```bash
go run src/main.go [port]
```

If `port` is not specified, it defaults to `8080`.

Example:
```bash
go run src/main.go 8081
```
The beacon will start listening on `http://localhost:8081`.

### Querying the Beacon

You can query the beacon using `curl` or any HTTP client.

1.  **Get current time (UTC ISO 8601 format):**
    ```bash
    curl http://localhost:8080/time
    # Example output: 2023-10-27T10:30:00.123456789Z
    ```

2.  **Introduce temporal drift:**
    Use the `drift` query parameter with a Go `time.Duration` string (e.g., `5s`, `-1m30s`, `2h`).
    ```bash
    # Time 10 seconds in the future
    curl "http://localhost:8080/time?drift=10s"

    # Time 5 minutes in the past
    curl "http://localhost:8080/time?drift=-5m"
    ```

3.  **Inject a temporal anomaly:**
    Use the `anomaly` query parameter. This will apply a *random* drift (between -1 hour and +1 hour) for *this single request only*.
    ```bash
    curl "http://localhost:8080/time?anomaly"
    ```
    You can combine `drift` and `anomaly`. The `anomaly` will be applied *after* the `drift`.
    ```bash
    curl "http://localhost:8080/time?drift=1h&anomaly"
    ```

## Development

### Prerequisites

- Go 1.18+

### Building

```bash
go build -o chronal-sync-beacon src/main.go
```

### Testing

```bash
go test ./tests/...
```
