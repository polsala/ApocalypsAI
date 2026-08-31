# Nightly Chrono-Ping Dispatcher

## Summary
Dispatches concurrent HTTP requests to multiple 'temporal anchors' (URLs), reporting their 'temporal stability' (response times and status codes).

## Description
In the fractured timelines of the ApocalypsAI, ensuring the stability of critical 'temporal anchors' (web services, APIs, data endpoints) is paramount. The Chrono-Ping Dispatcher sends out concurrent 'chrono-pings' to a list of specified URLs, measuring how quickly and reliably they respond. It's like sending probes into different temporal streams to check for echoes of existence, ensuring that your vital systems are still resonating in the present.

This utility is designed for quick, concurrent checks of multiple network endpoints, providing immediate feedback on their responsiveness and availability.

## Features
*   **Concurrent Pinging**: Efficiently checks multiple URLs simultaneously using Go's goroutines.
*   **Temporal Stability Metrics**: Reports HTTP status code, response time (latency), and any encountered errors for each 'temporal anchor'.
*   **Configurable Timeout**: Set a maximum duration for each chrono-ping to prevent indefinite waits.
*   **Flexible Input**: Provide URLs directly as command-line arguments or via a file.
*   **Whimsical Theme**: Integrates seamlessly into the ApocalypsAI universe with its 'temporal' terminology.

## Installation
To install the `chrono-ping-dispatcher` utility, ensure you have Go (1.16 or newer) installed.

```bash
# Clone the repository (if not already done)
# git clone https://github.com/polsala/ApocalypsAI.git
# cd ApocalypsAI/go-utils/nightly-chrono-ping-dispatcher

# Build and install the executable to your GOPATH/bin
go install ./src

# Or, build it locally
go build -o chrono-ping-dispatcher src/main.go
```

## Usage

### Pinging URLs directly from command-line arguments:
```bash
chrono-ping-dispatcher https://google.com https://github.com http://localhost:8080
```

### Pinging URLs from a file (one URL per line):
Create a file named `urls.txt`:
```
https://example.com
https://api.temporal-nexus.net/status
http://unstable-rift.local:9000
```
Then run:
```bash
chrono-ping-dispatcher -f urls.txt
```

### Specifying a custom timeout (e.g., 2 seconds):
```bash
chrono-ping-dispatcher -t 2s https://slow-anchor.org
```

### Example Output
```
Chrono-Ping Dispatcher initiating temporal probes...

Chrono-Ping Report:
-------------------
URL: https://google.com
  Status: 200 OK
  Latency: 50.123ms
  Error: <nil>

URL: https://github.com
  Status: 200 OK
  Latency: 75.456ms
  Error: <nil>

URL: http://unstable-rift.local:9000
  Status: 0
  Latency: 0s
  Error: Get "http://unstable-rift.local:9000": dial tcp 127.0.0.1:9000: connect: connection refused

URL: https://non-existent-temporal-anchor.com
  Status: 0
  Latency: 0s
  Error: Get "https://non-existent-temporal-anchor.com": dial tcp: lookup non-existent-temporal-anchor.com: no such host
-------------------
Report Complete. Temporal stability assessed.
```
