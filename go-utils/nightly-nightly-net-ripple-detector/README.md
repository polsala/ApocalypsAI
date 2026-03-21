# Nightly Net Ripple Detector

A Go-based concurrent network utility that detects "etheric ripples" by monitoring latency and response anomalies across specified network targets. It's designed to give early warnings about potential network disturbances before they escalate into full-blown temporal distortions.

## Features

*   **Concurrent Probing**: Efficiently checks multiple network targets simultaneously using Go's goroutines.
*   **Latency Monitoring**: Reports on response times and flags targets exceeding a configurable latency threshold.
*   **Status Code Analysis**: Identifies non-2xx HTTP responses as "unstable resonances."
*   **Connection Error Detection**: Flags unreachable targets or connection failures as critical "etheric ripples."
*   **Whimsical Reporting**: Provides status updates with a touch of ApocalypsAI flair.

## Usage

### Build

To build the utility, navigate to the `src` directory and run:

```bash
go build -o nightly-net-ripple-detector main.go
```

This will create an executable named `nightly-net-ripple-detector` in the current directory.

### Run

Execute the utility with one or more target URLs. You can also specify a custom timeout and latency threshold.

```bash
./nightly-net-ripple-detector <target1_url> [target2_url...] [--timeout=<ms>] [--threshold=<ms>]
```

**Arguments:**

*   `<target_url>`: One or more HTTP/HTTPS URLs to probe (e.g., `http://example.com`, `https://api.service.com`).
*   `--timeout=<ms>`: Optional. The maximum time in milliseconds to wait for a response from each target. Defaults to `5000`ms (5 seconds).
*   `--threshold=<ms>`: Optional. The latency threshold in milliseconds. If a target's response time exceeds this, it's flagged as a "temporal distortion." Defaults to `1000`ms (1 second).

**Examples:**

Check a single website with default settings:
```bash
./nightly-net-ripple-detector https://www.google.com
```

Check multiple services with a shorter timeout and stricter latency threshold:
```bash
./nightly-net-ripple-detector https://api.example.com https://dashboard.example.com --timeout=2000 --threshold=500
```

### Exit Codes

*   `0`: All network resonances are stable. No etheric ripples detected.
*   `1`: One or more etheric ripples detected in the network fabric.

## Development

### Running Tests

To run the automated tests, navigate to the root of the utility directory (`nightly-net-ripple-detector/`) and run:

```bash
go test ./...
```

The tests use `httptest.NewServer` to simulate network responses, ensuring they are deterministic and do not rely on external network access.
