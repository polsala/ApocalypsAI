# Nightly Chrono-Watchdog

The Nightly Chrono-Watchdog is a whimsical-yet-useful Go-based utility designed to monitor the temporal stability of your critical web resources. It periodically fetches content from a list of specified URLs, calculates a cryptographic hash of their content, and measures the response latency. If it detects any content changes or significant latency spikes, it reports these "temporal anomalies" to help you maintain the integrity and performance of your digital outposts in the wasteland.

## Features

*   **Concurrent Monitoring**: Efficiently checks multiple URLs simultaneously using Go's goroutines.
*   **Content Integrity**: Detects unauthorized or unexpected changes to web page content via SHA256 hashing.
*   **Latency Anomaly Detection**: Flags significant increases in response time (more than double the previous check), indicating potential performance degradation.
*   **Configurable**: Easily specify URLs and check intervals.
*   **Lightweight**: A self-contained Go binary, ideal for deployment in resource-constrained environments.

## Usage

### Prerequisites

*   Go (version 1.18 or higher)

### Build and Run

1.  **Navigate to the utility's directory:**
    ```bash
    # Assuming you are in the root of the ApocalypsAI repository
    cd go-utils/nightly-chrono-watchdog
    ```

2.  **Build the executable:**
    ```bash
    go build -o chrono-watchdog src/main.go
    ```

3.  **Run the utility:**
    Specify the URLs to monitor (comma-separated) and the check interval.

    ```bash
    ./chrono-watchdog -urls "https://example.com,https://www.google.com" -interval "30s"
    ```

    **Example Output:**
    ```
    2023/10/27 10:30:00 Starting Chrono-Watchdog for 2 URLs, checking every 30s
    2023/10/27 10:30:00 [INFO] Initial check for https://example.com: Hash=a1b2c3d4..., Latency=123ms
    2023/10/27 10:30:01 [INFO] Initial check for https://www.google.com: Hash=e5f6g7h8..., Latency=456ms
    2023/10/27 10:30:30 [INFO] https://example.com: No significant changes. Hash=a1b2c3d4..., Latency=120ms
    2023/10/27 10:30:31 [ANOMALY] Content change detected for https://www.google.com!
      Old Hash: e5f6g7h8...
      New Hash: i9j0k1l2...
      Latency: 460ms
    2023/10/27 10:31:00 [ANOMALY] Significant latency increase for https://example.com!
      Old Latency: 120ms
      New Latency: 300ms
      Content Hash: a1b2c3d4...
    ```

### Command-line Arguments

*   `-urls`: **Required.** A comma-separated list of URLs to monitor.
    *   Example: `https://my-api.com/health,https://my-blog.org/status`
*   `-interval`: **Optional.** The duration between checks. Defaults to `1m` (1 minute).
    *   Supported units: `s` (seconds), `m` (minutes), `h` (hours).
    *   Example: `10s`, `5m`, `1h`

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
go test ./tests/...
```

The tests use a mocked HTTP client to ensure determinism and avoid actual network calls.
