# nightly-beacon-pulse-monitor

A Go CLI tool designed to concurrently monitor the "pulse" of critical network "beacons" (URLs or TCP ports) across the digital wasteland. It reports on their vitality, response times, and overall status, helping you ensure your essential services are still "pulsing strongly" in the post-apocalyptic network landscape.

## Features

*   **Concurrent Monitoring**: Checks multiple targets simultaneously using Go's goroutines.
*   **HTTP/HTTPS Support**: Performs GET requests and reports HTTP status codes.
*   **TCP Port Checking**: Attempts to establish a TCP connection to verify port availability.
*   **Response Time Measurement**: Tracks how long each beacon takes to respond.
*   **Configurable Timeout**: Set a maximum wait time for each beacon.
*   **Whimsical Output**: Reports beacon status with themed messages.

## Installation

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-beacon-pulse-monitor
    ```
3.  **Build the utility**:
    ```bash
    go build -o beacon-pulse-monitor src/main.go
    ```
    This will create an executable named `beacon-pulse-monitor` in the current directory.

## Usage

Run the executable with a list of targets. Targets can be HTTP/HTTPS URLs or TCP addresses in the format `tcp:host:port`.

```bash
./beacon-pulse-monitor -targets "http://google.com,https://github.com,tcp:localhost:8080" -timeout 5s
```

### Arguments

*   `-targets <comma-separated-list>`: A comma-separated list of URLs or `tcp:host:port` strings to monitor.
    *   Example: `"http://example.com,https://api.example.com,tcp:127.0.0.1:22"`
*   `-timeout <duration>`: The maximum time to wait for each beacon to respond (e.g., `1s`, `500ms`). Default is `3s`.

## Examples

1.  **Check a few web services and a local SSH port:**
    ```bash
    ./beacon-pulse-monitor -targets "http://example.com,https://api.github.com,tcp:localhost:22"
    ```

2.  **With a shorter timeout:**
    ```bash
    ./beacon-pulse-monitor -targets "http://slow-service.com,tcp:remote-host:80" -timeout 1s
    ```

## Output Interpretation

*   **Pulsing strongly!**: The beacon responded successfully within the timeout.
*   **Faint signal...**: The beacon responded, but with a non-ideal status (e.g., HTTP 4xx/5xx).
*   **Flatlined!**: The beacon did not respond, timed out, or connection was refused.

## Development

To run tests:

```bash
go test ./tests/...
```
