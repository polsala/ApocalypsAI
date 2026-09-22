# Nightly Chrono-Sync Beacon

## Summary

The `nightly-chrono-sync-beacon` is a whimsical-yet-useful Go-based command-line utility designed to help maintain temporal alignment across your distributed services. It acts as a "temporal alignment signal broadcaster," concurrently probing specified service endpoints and reporting on any "chronological drift" detected relative to the beacon's local time.

Think of it as a cosmic clock-watcher, ensuring all your digital cogs are turning in harmonious synchronicity, preventing temporal anomalies before they become full-blown paradoxes.

## How it Works

1.  **Endpoint Probing**: The beacon takes a list of URLs as arguments. These URLs are expected to be simple HTTP endpoints that return their current time in ISO 8601 format (e.g., `2006-01-02T15:04:05Z07:00`).
2.  **Concurrent Checks**: For each endpoint, a separate Go goroutine is launched to perform the check concurrently.
3.  **Drift Calculation**: Each goroutine records the beacon's local time before making the request. Upon receiving the service's time, it calculates the difference, accounting for a simulated network latency (or assuming negligible for simplicity in this whimsical context).
4.  **Reporting**: The utility prints a report for each service, indicating its reported time, the calculated drift, and a status (e.g., "Aligned," "Slight Drift," "Significant Drift").

## Usage

### Prerequisites

-   Go (version 1.18 or higher)

### Build

```bash
go build -o chrono-sync-beacon src/main.go
```

### Run

```bash
./chrono-sync-beacon <endpoint1_url> [endpoint2_url ...]
```

**Example:**

```bash
# Assuming you have services running at these endpoints that return their current time
./chrono-sync-beacon http://localhost:8080/time http://localhost:8081/time
```

### Expected Endpoint Response Format

Your service endpoints should respond to a `GET` request with a plain text body containing the current time in ISO 8601 format. For example:

```
2023-10-27T10:30:00Z
```

## Configuration

Currently, configuration is via command-line arguments. Future enhancements might include a configuration file for more complex scenarios.

## Development & Testing

To run the tests:

```bash
go test ./tests/...
```
