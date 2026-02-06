# Nightly Chronal Resonance Pinger

## Overview

The `nightly-chronal-resonance-pinger` is a whimsical-yet-useful Go utility designed to monitor the "chronal resonance" of various network endpoints. In simpler terms, it concurrently pings a list of specified URLs or IP addresses, measures their response times (their "temporal resonance"), and reports on the overall "temporal stability" of your digital infrastructure.

This tool helps identify slow-responding services, network bottlenecks, or outright failures, presenting them as "temporal anomalies" in a concise report.

## Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to ping multiple targets simultaneously, making it efficient for monitoring many services.
*   **Temporal Resonance Measurement**: Accurately measures the time taken for each endpoint to respond.
*   **Anomaly Detection**: Clearly distinguishes between successful resonances and "temporal anomalies" (failed pings or HTTP errors).
*   **Summary Report**: Provides an average resonance time for successful pings and detailed error messages for failures.
*   **Configurable Timeout**: Each ping attempt has a default 5-second timeout to prevent indefinite waits.

## Installation

To install the utility, ensure you have Go (version 1.16 or higher) installed.

1.  Clone the `polsala/ApocalypsAI` repository (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
2.  Navigate to the utility's directory:
    ```bash
    cd go-utils/nightly-chronal-resonance-pinger
    ```
3.  Build the executable:
    ```bash
    go build -o nightly-chronal-resonance-pinger src/main.go
    ```

This will create an executable named `nightly-chronal-resonance-pinger` in the current directory.

## Usage

Run the utility by providing one or more target URLs or IP addresses as command-line arguments:

```bash
./nightly-chronal-resonance-pinger <target_url_1> [target_url_2 ...]
```

**Examples:**

*   Ping a single website:
    ```bash
    ./nightly-chronal-resonance-pinger https://www.google.com
    ```

*   Ping multiple services:
    ```bash
    ./nightly-chronal-resonance-pinger https://api.example.com http://localhost:8080 https://unreachable.domain
    ```

*   Ping a local IP address (ensure it's serving HTTP):
    ```bash
    ./nightly-chronal-resonance-pinger http://192.168.1.1
    ```

### Output Interpretation

The report will categorize results:

*   **Successful Resonances**: Endpoints that responded successfully, showing their target and the measured duration.
*   **Average Resonance Time**: The average response time across all successful pings.
*   **Temporal Anomalies (Failed Resonances)**: Endpoints that failed to respond, timed out, or returned an HTTP error (4xx/5xx), along with the error message and the duration until the error was detected.

## Development

### Running Tests

To ensure the utility is functioning correctly, run the provided tests:

```bash
cd go-utils/nightly-chronal-resonance-pinger
go test ./tests/...
```

The tests use `httptest.NewServer` to create mock HTTP servers, ensuring they are deterministic and do not rely on external network access.
