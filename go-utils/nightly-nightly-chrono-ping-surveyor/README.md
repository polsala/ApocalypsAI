# Nightly Chrono-Ping Surveyor

The Nightly Chrono-Ping Surveyor is a whimsical-yet-critical utility designed to detect "temporal distortions" across your network infrastructure. In the post-apocalyptic landscape, stable network connectivity is paramount. This tool concurrently pings a list of specified HTTP/HTTPS endpoints, measuring their response times and highlighting any significant delays that might indicate a temporal anomaly or, more prosaically, network latency.

## Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to ping multiple targets simultaneously for efficient surveying.
*   **Temporal Distortion Detection**: Flags response times exceeding a configurable threshold as "temporal distortions."
*   **Clear Reporting**: Provides a summary of all pings, their durations, and highlights any detected anomalies.
*   **Configurable Timeout**: Prevents indefinite waits for unresponsive endpoints.

## Usage

### Build

```bash
go build -o chrono-ping-surveyor src/main.go
```

### Run

```bash
./chrono-ping-surveyor -timeout 5s -threshold 200ms https://example.com http://localhost:8080 https://api.service.io
```

**Arguments:**

*   `-timeout <duration>`: Maximum time to wait for a single endpoint response (e.g., `5s`, `100ms`). Default is `5s`.
*   `-threshold <duration>`: Response time above which an endpoint is considered to have a "temporal distortion" (e.g., `200ms`, `1s`). Default is `100ms`.
*   `<urls...>`: One or more HTTP/HTTPS URLs to ping.

### Example Output

```
[2024-07-30 22:00:00] Chrono-Ping Survey Report:
--------------------------------------------------
[OK] https://example.com - 55ms
[OK] http://localhost:8080 - 2ms
[DISTORTION!] https://api.service.io - 1234ms (Threshold: 200ms)
[ERROR] http://unreachable.host - Failed to connect: dial tcp: lookup unreachable.host: no such host
--------------------------------------------------
Survey Complete. Detected 1 Temporal Distortion.
```

## Development

To run tests:

```bash
go test ./tests/...
```
