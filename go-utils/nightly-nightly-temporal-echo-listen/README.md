# ApocalypsAI Temporal Echo Listener

## Overview

The `nightly-temporal-echo-listener` is a whimsical-yet-useful Go utility designed to simulate a distributed system's time-sensitive data processing. It acts as a UDP server, listening for incoming "temporal echoes" – simple messages containing a timestamp, a unique message ID, and a payload. Using Go's concurrency features, it processes these echoes to detect and log potential "time-anomalies" and "echo duplications."

This tool can be used to:
- Demonstrate a basic concurrent UDP server in Go.
- Simulate monitoring for out-of-order or duplicate messages in a distributed environment.
- Provide a fun, themed utility for the ApocalypsAI community.

## Features

- **UDP Listener**: Listens on a configurable UDP port for incoming messages.
- **Concurrent Processing**: Utilizes Go goroutines and channels for efficient, concurrent handling of multiple echoes.
- **Temporal Drift Detection**: Identifies messages whose timestamps are significantly in the past or future relative to the listener's current time.
- **Echo Duplication Detection**: Flags messages with the same ID received within a short, configurable time window.
- **Configurable Thresholds**: `DUPLICATE_WINDOW` and `TEMPORAL_DRIFT_THRESHOLD` can be adjusted.

## Message Format

Incoming UDP messages are expected to follow this format:

`timestamp_ms|message_id|payload`

- `timestamp_ms`: The Unix timestamp of when the message was sent, in milliseconds.
- `message_id`: A unique identifier for the message (e.g., `event-123`, `sensor-reading-XYZ`).
- `payload`: Any string data associated with the echo.

**Example:** `1678886400000|echo-alpha-7|Hello from the past!`

## Installation & Usage

### Prerequisites

- Go (version 1.18 or higher)

### Build

```bash
cd nightly-temporal-echo-listener/src
go build -o ../bin/temporal-echo-listener .
```

### Run

```bash
# Navigate to the utility's root directory
cd nightly-temporal-echo-listener

# Run with default port (8080)
./bin/temporal-echo-listener

# Or specify a different port using an environment variable
PORT=9000 ./bin/temporal-echo-listener
```

The listener will start and print a message indicating the port it's listening on.

### Sending Echoes (Testing)

You can send UDP messages using `netcat` (or `nc`) or a simple Go/Python script.

**Using `netcat`:**

```bash
# Send a normal echo
echo "$(date +%s%3N)|normal-echo-1|All is well" | nc -u -w0 127.0.0.1 8080

# Send an echo from the future (adjust timestamp)
echo "$(($(date +%s%3N) + 20000))|future-echo-1|I see tomorrow!" | nc -u -w0 127.0.0.1 8080

# Send an echo from the past (adjust timestamp)
echo "$(($(date +%s%3N) - 20000))|past-echo-1|Remember yesterday?" | nc -u -w0 127.0.0.1 8080

# Send a duplicate echo quickly
echo "$(date +%s%3N)|duplicate-echo-1|First instance" | nc -u -w0 127.0.0.1 8080
sleep 1 # Wait a bit, but less than DUPLICATE_WINDOW (default 5s)
echo "$(date +%s%3N)|duplicate-echo-1|Second instance" | nc -u -w0 127.0.0.1 8080
```

Observe the console output of the `temporal-echo-listener` for anomaly reports.

## Configuration

You can adjust the anomaly detection thresholds by modifying the `const` values in `src/main.go`:

- `duplicateWindow`: The duration within which two messages with the same `message_id` are considered duplicates (default: 5 seconds).
- `temporalDriftThreshold`: The maximum allowed difference between the message's timestamp and the listener's current time before it's flagged as a temporal drift anomaly (default: 10 seconds).

## Development

### Running Tests

```bash
cd nightly-temporal-echo-listener/tests
go test -v .
```

Tests cover message parsing, anomaly detection logic, and concurrent processing using mocked network connections and time providers for deterministic results.
