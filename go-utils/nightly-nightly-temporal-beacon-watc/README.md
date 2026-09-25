# Nightly Temporal Beacon Watcher

A Go-based concurrent network utility designed to monitor multiple 'temporal beacons' (network endpoints/URLs) for their operational status and latency. It provides a quick overview of which services are `Steady`, `Lagging`, or `Silent`.

## Whimsical Purpose

In the vast, ever-shifting landscape of the post-apocalyptic digital realm, critical data beacons flicker across the network. This utility acts as your vigilant watchman, ensuring that these vital signals remain `Steady`, warning you if they become `Lagging`, and alerting you immediately if they fall `Silent`. Never again be caught unaware by a failing distant outpost!

## Features

*   **Concurrent Monitoring**: Checks multiple URLs simultaneously using Go's goroutines.
*   **Status Reporting**: Categorizes beacons as `Steady` (responsive, low latency), `Lagging` (responsive, high latency), or `Silent` (unresponsive or error).
*   **Configurable Timeout**: Set a maximum duration for each beacon check.
*   **Clear Output**: Provides an easy-to-read report with status emojis and latency details.

## Installation

1.  **Ensure Go is installed**: If you don't have Go, download and install it from [golang.org](https://golang.org/doc/install).
2.  **Clone the repository (if not already done)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-temporal-beacon-watcher
    ```
3.  **Build the utility**:
    ```bash
    go build -o beacon-watcher src/main.go
    ```

## Usage

Run the `beacon-watcher` executable with a comma-separated list of endpoints and an optional timeout.

```bash
./beacon-watcher -endpoints "http://google.com,http://example.com,http://nonexistent.domain,http://localhost:8080" -timeout 3
```

### Arguments:

*   `-endpoints` (required): A comma-separated string of URLs to monitor.
*   `-timeout` (optional): Timeout for each beacon check in seconds. Defaults to `5` seconds.

### Example Output:

```
Monitoring 4 temporal beacons with a 3s timeout per beacon...

--- Temporal Beacon Report ---
🟢 Steady     http://google.com                        Latency: 50ms
🟢 Steady     http://example.com                       Latency: 20ms
🔴 Silent     http://nonexistent.domain                Latency: 3s         (Error: Get "http://nonexistent.domain": dial tcp: lookup nonexistent.domain: no such host)
🔴 Silent     http://localhost:8080                    Latency: 3s         (Error: Get "http://localhost:8080": dial tcp 127.0.0.1:8080: connect: connection refused)
------------------------------
```

## Development

To run tests:

```bash
cd go-utils/nightly-temporal-beacon-watcher
go test ./tests/...
```
