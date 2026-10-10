# Nightly Cosmic Echo Listener

A Go-based utility designed to detect subtle network 'echoes' and emit 'whispers' across the digital void. This tool acts as a simple UDP listener and sender, perfect for lightweight network presence detection, inter-service communication, or just adding a touch of cosmic mystery to your infrastructure.

## Features

*   **Echo Listener**: Listens on a specified UDP port for incoming messages (cosmic echoes).
*   **Whisper Sender**: Periodically sends configurable UDP messages (cosmic whispers) to a target address.
*   **Concurrent**: Utilizes Go's goroutines for efficient, non-blocking operation.
*   **Configurable**: Easily adjust listen port, target address, whisper interval, and message content via environment variables.

## How to Use

### Prerequisites

*   Go (version 1.20 or higher)

### Build and Run

1.  **Navigate to the utility directory:**
    ```bash
    cd go-utils/nightly-cosmic-echo-listener
    ```

2.  **Build the executable:**
    ```bash
    go build -o cosmic-echo-listener src/main.go
    ```

3.  **Run the utility:**

    *   **As a listener only (default):**
        ```bash
        ./cosmic-echo-listener
        # Listens on UDP port 8080 by default.
        ```

    *   **As a listener and sender (to another instance or target):**
        ```bash
        LISTEN_PORT=8081 ECHO_TARGET="127.0.0.1:8080" WHISPER_INTERVAL_SECONDS=5 WHISPER_MESSAGE="Are you out there?" ./cosmic-echo-listener
        # Listens on 8081, sends whispers to 127.0.0.1:8080 every 5 seconds.
        ```

    *   **Example: Run two instances to see them communicate:**

        **Terminal 1 (Listener & Sender A):**
        ```bash
        LISTEN_PORT=8080 ECHO_TARGET="127.0.0.1:8081" WHISPER_INTERVAL_SECONDS=3 WHISPER_MESSAGE="Echo from Sector Alpha" ./cosmic-echo-listener
        ```

        **Terminal 2 (Listener & Sender B):**
        ```bash
        LISTEN_PORT=8081 ECHO_TARGET="127.0.0.1:8080" WHISPER_INTERVAL_SECONDS=5 WHISPER_MESSAGE="Reply from Sector Beta" ./cosmic-echo-listener
        ```
        You will see logs in both terminals indicating received echoes and sent whispers.

### Configuration

The utility can be configured using the following environment variables:

*   `LISTEN_PORT`: The UDP port to listen for incoming echoes. (Default: `8080`)
*   `ECHO_TARGET`: The `IP:Port` address to send periodic whispers to. If not set, no whispers will be sent. (Default: `""`)
*   `WHISPER_INTERVAL_SECONDS`: The interval (in seconds) between sending whispers. (Default: `30`)
*   `WHISPER_MESSAGE`: The content of the cosmic whisper message. (Default: `"A faint cosmic whisper..."`)

## Development

### Running Tests

To run the automated tests:

```bash
cd go-utils/nightly-cosmic-echo-listener
go test ./tests/...
```

Tests are designed to be deterministic and run offline, simulating network interactions using local loopback addresses.
