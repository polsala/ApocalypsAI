# Nightly Chrono-Sync Beacon

## Overview

The `nightly-chrono-sync-beacon` is a whimsical-yet-useful Go utility designed to monitor the 'temporal harmony' of your network endpoints. Instead of mundane 'up/down' checks, this beacon measures response latencies and reports on whether your services are in 'Temporal Harmony', experiencing 'Slight Chronal Anomalies', suffering from 'Severe Time Dilation', or are 'Lost in the Void'.

It's perfect for quickly assessing the responsiveness of multiple critical services concurrently, providing a fun and insightful snapshot of your system's temporal state.

## Features

*   **Concurrent Checks**: Utilizes Go's goroutines to check multiple endpoints simultaneously.
*   **Whimsical Status Reports**: Translates latency into engaging temporal metaphors.
*   **Configurable Thresholds**: Define expected maximum durations for each endpoint.
*   **Clear Output**: Provides a summary of each endpoint's temporal status.

## Installation

1.  **Clone the repository (if not already in the ApocalypsAI structure):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chrono-sync-beacon
    ```
2.  **Build the executable:**
    ```bash
    go build -o chrono-sync-beacon src/main.go
    ```

## Usage

Run the beacon with a list of targets. Targets are defined within the `src/main.go` file for simplicity in this standalone utility. You can modify the `targets` slice directly.

```bash
./chrono-sync-beacon
```

### Example Output

```
Initiating Chrono-Sync Scan...

[http://localhost:8080/status] Temporal Harmony (55ms)
[https://api.example.com/health] Slight Chronal Anomaly (180ms, expected <100ms)
[http://internal-service:9000/metrics] Severe Time Dilation (320ms, expected <50ms)
[http://nonexistent.local] Lost in the Void (dial tcp: lookup nonexistent.local: no such host)

Chrono-Sync Scan Complete. All temporal anomalies logged.
```

## Configuration

Currently, targets and their expected durations are hardcoded within `src/main.go` for simplicity. To modify:

Open `src/main.go` and edit the `targets` slice:

```go
var targets = []Target{
    {URL: "http://localhost:8080/status", ExpectedMaxDurationMs: 100},
    {URL: "https://api.example.com/health", ExpectedMaxDurationMs: 100},
    {URL: "http://internal-service:9000/metrics", ExpectedMaxDurationMs: 50},
    {URL: "http://nonexistent.local", ExpectedMaxDurationMs: 50},
}
```

*   `URL`: The endpoint to check.
*   `ExpectedMaxDurationMs`: The maximum acceptable response time in milliseconds for 'Temporal Harmony'.

### Temporal Anomaly Thresholds

The utility uses internal thresholds to classify anomalies:

*   **Slight Chronal Anomaly**: Response time is between `ExpectedMaxDurationMs` and `ExpectedMaxDurationMs * SlightAnomalyFactor` (default: 1.5x).
*   **Severe Time Dilation**: Response time is greater than `ExpectedMaxDurationMs * SevereDilationFactor` (default: 3x).

These factors can be adjusted in `src/main.go` if needed.

## Development

### Running Tests

To ensure the beacon is functioning correctly, run the provided tests:

```bash
cd go-utils/nightly-chrono-sync-beacon
go test ./tests/...
```

Tests use a mocked HTTP client to simulate various network conditions (fast, slow, error) deterministically.
