# Nightly Chrono-Sync Beacon

## Overview

The `nightly-chrono-sync-beacon` is a whimsical-yet-useful Go-based HTTP service designed to provide a community-agreed time signal. In a world where temporal anomalies might cause local clocks to drift, this beacon offers a centralized, albeit sometimes playfully 'drifted', time source. It's perfect for synchronizing distributed systems, performing network health checks, or simply adding a touch of temporal uncertainty to your day.

## Features

- **Current UTC Time**: Provides the precise current UTC time.
- **Configurable Temporal Drift**: Allows clients to request a time with an intentional millisecond offset, simulating minor temporal distortions.
- **Simple HTTP API**: Easy to integrate with `curl`, `wget`, or any HTTP client.
- **Lightweight & Concurrent**: Built with Go's excellent concurrency model for efficient operation.

## Usage

### 1. Build the Utility

Navigate to the `src` directory and build the Go application:

```bash
cd go-utils/nightly-chrono-sync-beacon/src
go build -o chrono-sync-beacon .
```

### 2. Run the Beacon

Execute the compiled binary. By default, it runs on port `8080`.

```bash
./chrono-sync-beacon
# Or specify a different port:
./chrono-sync-beacon -port 8081
```

### 3. Query the Time

Use `curl` or your preferred HTTP client to get the current time:

```bash
# Get current UTC time (no drift)
curl http://localhost:8080/time
# Expected output (timestamp will vary):
# {"timestamp":"2023-10-27T10:30:00.123456789Z","message":"Time signal from the Chrono-Sync Beacon. May contain temporal whimsy.","drift_ms":0}

# Get current UTC time with a positive drift of 500 milliseconds
curl http://localhost:8080/time?drift_ms=500
# Expected output (timestamp will be ~500ms in the future):
# {"timestamp":"2023-10-27T10:30:00.623456789Z","message":"Time signal from the Chrono-Sync Beacon. May contain temporal whimsy.","drift_ms":500}

# Get current UTC time with a negative drift of 1000 milliseconds (1 second in the past)
curl http://localhost:8080/time?drift_ms=-1000
# Expected output (timestamp will be ~1s in the past):
# {"timestamp":"2023-10-27T10:29:59.123456789Z","message":"Time signal from the Chrono-Sync Beacon. May contain temporal whimsy.","drift_ms":-1000}

# Check the beacon's operational status
curl http://localhost:8080/status
# Expected output:
# {"message":"Chrono-Sync Beacon is humming along, broadcasting temporal truths (mostly).","status":"Operational","uptime":"..."}
```

## Development

### Running Tests

To run the automated tests, navigate to the utility's root directory and use `go test`:

```bash
cd go-utils/nightly-chrono-sync-beacon
go test ./tests/...
```

### Configuration

The beacon can be configured via command-line flags:

- `--port <number>`: Specifies the port the server will listen on (default: `8080`).

## Contributing

Feel free to suggest improvements or new whimsical temporal features!
