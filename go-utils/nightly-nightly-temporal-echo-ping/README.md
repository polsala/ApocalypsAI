# Nightly Temporal Echo Ping

A Go-based concurrent network utility designed to monitor the "temporal stability" (latency) of various "temporal anchors" (network endpoints). It detects "echoes" (latency anomalies) and reports on the overall timeline's integrity.

## Purpose

In the ApocalypsAI universe, maintaining the stability of critical systems is paramount. This utility helps monitor the responsiveness of key network services, imaginatively dubbed "temporal anchors," by concurrently pinging them and reporting on their latency. If a "temporal anchor" experiences high latency beyond a configurable threshold, it's flagged as an "echo," indicating potential "temporal flux" that requires investigation.

## Features

*   **Concurrent Monitoring**: Pings multiple temporal anchors simultaneously using Go's goroutines.
*   **Latency Reporting**: Measures and reports the round-trip time for each anchor.
*   **Echo Detection**: Flags anchors experiencing latency above a defined "echo threshold."
*   **Configurable**: Targets, ping timeout, and echo threshold are configurable via environment variables.
*   **Whimsical Output**: Provides status updates with an apocalyptic flair.

## Usage

### Prerequisites

*   Go (version 1.16 or higher) installed.

### Build and Run

1.  Navigate to the `src` directory:
    ```bash
    cd go-utils/nightly-temporal-echo-ping/src
    ```
2.  Build the executable:
    ```bash
    go build -o ../temporal-echo-ping .
    ```
3.  Run the utility. You can configure it using environment variables:

    *   `TEMPORAL_ANCHORS`: A comma-separated list of `Name=URL` pairs for the anchors to monitor.
        *   Example: `Void Gate=http://localhost:8080/void,Rift Stabilizer=http://127.0.0.1:9000/rift`
    *   `PING_TIMEOUT_MS`: The maximum time (in milliseconds) to wait for a ping response. Defaults to `5000` (5 seconds).
    *   `ECHO_THRESHOLD_MS`: The latency threshold (in milliseconds) above which a ping is considered an "echo." Defaults to `200` (200ms).

    **Example Run:**
    ```bash
    TEMPORAL_ANCHORS="Void Gate=https://www.google.com,Temporal Nexus=https://www.github.com" \
    PING_TIMEOUT_MS="2000" \
    ECHO_THRESHOLD_MS="100" \
    ../temporal-echo-ping
    ```

    If no `TEMPORAL_ANCHORS` are provided, it defaults to `Void Gate=http://localhost:8080/void,Rift Stabilizer=http://localhost:8081/rift`. These default targets are likely to fail unless you have local services running, which is useful for testing error states.

### Expected Output

```
Monitoring 2 temporal anchors for stability...
Ping Timeout: 2s, Echo Threshold: 100ms

--- Temporal Stability Report ---
  [OK]    Void Gate: Temporal stability maintained. Latency: 25.123ms
  [ECHO!] Temporal Nexus: Experiencing temporal flux! Latency: 123.456ms (exceeds 100ms)

Warning: Some temporal anchors are experiencing echoes. Investigation recommended.
```

Or, if all is stable:

```
Monitoring 2 temporal anchors for stability...
Ping Timeout: 2s, Echo Threshold: 100ms

--- Temporal Stability Report ---
  [OK]    Void Gate: Temporal stability maintained. Latency: 25.123ms
  [OK]    Temporal Nexus: Temporal stability maintained. Latency: 45.678ms

All temporal anchors are stable. The timeline holds... for now.
```

The utility exits with status `0` if all anchors are stable, and `1` if any echoes or errors are detected.

## Development

### Running Tests

From the utility's root directory (`go-utils/nightly-temporal-echo-ping/`):

```bash
go test ./tests/...
```

The tests use `net/http/httptest` to create local mock HTTP servers, ensuring they are deterministic and do not rely on external network access.
