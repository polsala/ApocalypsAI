# Nightly Temporal Echo Listener

## Summary

The `nightly-temporal-echo-listen` is a whimsical-yet-useful Go-based network utility designed to simulate temporal anomalies in communication. It listens on a specified TCP port, receives incoming messages, applies a configurable "temporal distortion" (delay and/or message reversal), and then echoes the distorted message back to the sender. This can be used for testing network resilience, simulating latency, or simply for fun.

## Features

*   **Configurable Port**: Listen on any available TCP port.
*   **Echo Delay**: Introduce a delay before echoing the message back.
*   **Message Reversal**: Reverse the received message before echoing it.
*   **Concurrent Handling**: Handles multiple client connections concurrently using Go's goroutines.
*   **Environment Variable Configuration**: Easy setup via environment variables.

## Usage

### Build

To build the utility, navigate to the `src` directory and run:

```bash
go build -o temporal-echo-listener main.go
```

This will create an executable named `temporal-echo-listener` in the `src` directory.

### Run

Run the compiled executable. Configuration is done via environment variables.

```bash
# Example: Run with default settings (port 8080, no delay, no reversal)
./temporal-echo-listener

# Example: Run with a 500ms delay on port 9000
PORT=9000 ECHO_DELAY_MS=500 ./temporal-echo-listener

# Example: Run with message reversal on port 8080
ECHO_REVERSE=true ./temporal-echo-listener

# Example: Run with 200ms delay and message reversal on port 8080
ECHO_DELAY_MS=200 ECHO_REVERSE=true ./temporal-echo-listener
```

### Configuration

The utility can be configured using the following environment variables:

*   `PORT`: The TCP port to listen on. Defaults to `8080` if not set or invalid.
*   `ECHO_DELAY_MS`: The delay in milliseconds before echoing the message. Defaults to `0` (no delay) if not set or invalid.
*   `ECHO_REVERSE`: Set to `true` to reverse the message before echoing. Defaults to `false`.

### Interacting with the Listener

You can interact with the `Temporal Echo Listener` using `netcat` or any TCP client.

```bash
# Connect to the listener (assuming it's running on port 8080)
netcat localhost 8080

# Type a message and press Enter
hello world

# The listener will echo back the (potentially distorted) message
# (e.g., if ECHO_REVERSE=true, you might see 'dlrow olleh')
```

## Development

### Project Structure

```
nightly-temporal-echo-listen/
├── README.md
├── src/
│   └── main.go
└── tests/
    └── temporal_echo_listener_test.go
```

### Dependencies

This utility uses only standard Go libraries. No external dependencies are required.

### Testing

To run the tests, navigate to the `tests` directory and execute:

```bash
go test -v
```

The tests cover various scenarios including no distortion, delay only, reversal only, and a combination of both, as well as concurrent connections and environment variable configuration. They use dynamic ports and `context` for graceful server shutdown to ensure determinism and isolation.
