# Nightly Cosmic Chronosync

## Overview

The `nightly-cosmic-chronosync` is a whimsical-yet-useful Go utility designed to provide a highly accurate and resilient time synchronization service. It acts as a local chronometer, querying multiple Network Time Protocol (NTP) servers concurrently, calculating a "consensus" time (the median of valid responses), and exposing this information via a simple HTTP API.

This utility is invaluable for distributed systems, microservices, or any application where precise time synchronization is critical, or where detecting discrepancies across various time sources is important for anomaly detection.

## Features

*   **Concurrent NTP Queries**: Fetches time from multiple NTP servers simultaneously using Go's goroutines.
*   **Consensus Time Calculation**: Determines a robust consensus time by taking the median of all successful NTP responses, mitigating the impact of individual faulty or slow servers.
*   **HTTP API**: Exposes the consensus time and detailed source information via a `/sync` endpoint.
*   **Configurable**: NTP servers and listening port can be configured via environment variables.
*   **Resilient**: Handles individual NTP server failures gracefully.

## Usage

### Prerequisites

*   Go (version 1.18 or higher)

### Building

To build the executable:

```bash
go build -o chronosync src/main.go
```

### Running

Run the compiled executable. You can configure the listening port and the list of NTP servers using environment variables:

```bash
# Example: Run on port 8081 with custom NTP servers
CHRONOSYNC_PORT=8081 CHRONOSYNC_NTP_SERVERS="time.cloudflare.com,time.google.com,pool.ntp.org" ./chronosync

# Default: Runs on port 8080 with default NTP servers (pool.ntp.org, time.google.com, time.nist.gov)
./chronosync
```

Once running, the service will listen for HTTP requests.

### API Endpoint

Query the `/sync` endpoint to get the current consensus time and details from each NTP source:

```bash
curl http://localhost:8080/sync
```

#### Example Response:

```json
{
  "consensus_time": "2023-10-27T10:00:00.123456789Z",
  "source_times": [
    {
      "server": "pool.ntp.org",
      "time": "2023-10-27T10:00:00.123456780Z",
      "error": ""
    },
    {
      "server": "time.google.com",
      "time": "2023-10-27T10:00:00.123456795Z",
      "error": ""
    },
    {
      "server": "time.nist.gov",
      "time": "2023-10-27T10:00:00.123456790Z",
      "error": ""
    },
    {
      "server": "invalid.ntp.server",
      "time": "0001-01-01T00:00:00Z",
      "error": "dial udp: lookup invalid.ntp.server: no such host"
    }
  ]
}
```

## Configuration

*   `CHRONOSYNC_PORT`: The port the HTTP server will listen on. Defaults to `8080`.
*   `CHRONOSYNC_NTP_SERVERS`: A comma-separated list of NTP server hostnames or IP addresses. Defaults to `pool.ntp.org,time.google.com,time.nist.gov`.

## Development

### Running Tests

```bash
go test ./tests/...
```

Tests are designed to be deterministic and offline, using mocks for NTP server interactions. See `tests/main_test.go` for details.
