# Nightly Beacon Broadcast

## Overview

The `nightly-beacon-broadcast` utility is a simple, Go-based concurrent service designed to send and receive encrypted status messages over UDP. It can operate in two modes: `broadcaster` or `listener`.

- **Broadcaster**: Periodically sends a small, encrypted "heartbeat" message to a list of configured UDP listener addresses. This can be used for basic health checks, presence signaling, or simple distributed messaging.
- **Listener**: Listens on a specified UDP port for incoming encrypted beacon messages, decrypts them, and prints the content to the console.

Messages are encrypted using a basic XOR cipher with a configurable shared key, providing a whimsical layer of "security" suitable for the ApocalypsAI community.

## Features

*   **Concurrent**: Leverages Go's goroutines for efficient, non-blocking network operations.
*   **UDP-based**: Uses User Datagram Protocol for lightweight, fire-and-forget messaging.
*   **Configurable**: Easily set port, broadcast interval, encryption key, and target addresses via command-line flags.
*   **Simple Encryption**: A basic XOR cipher for message obfuscation (not for high-security applications).
*   **Self-contained**: Single Go executable for both broadcaster and listener modes.

## Installation

To build the utility, ensure you have Go (1.16 or newer) installed.

```bash
cd go-utils/nightly-beacon-broadcast
go build -o beacon-broadcast src/main.go
```

This will create an executable named `beacon-broadcast` in the current directory.

## Usage

### Broadcaster Mode

To start the broadcaster, specify the `mode` as `broadcaster` and provide a comma-separated list of target `targets`.

```bash
./beacon-broadcast --mode broadcaster \
                   --port 8080 \
                   --interval 5s \
                   --key "apocalypsai" \
                   --targets "127.0.0.1:8081,192.168.1.100:8082"
```

**Arguments:**

*   `--mode`: Must be `broadcaster`.
*   `--port` (optional): The local UDP port to bind to for sending messages. Default: `8080`.
*   `--interval` (optional): How often to send a beacon message (e.g., `1s`, `30s`, `1m`). Default: `5s`.
*   `--key` (optional): The shared encryption key for the XOR cipher. Default: `apocalypsai`.
*   `--targets`: A comma-separated list of `IP:Port` addresses where beacon messages should be sent. **Required** for broadcaster mode.

### Listener Mode

To start the listener, specify the `mode` as `listener` and the port it should listen on.

```bash
./beacon-broadcast --mode listener \
                   --port 8081 \
                   --key "apocalypsai"
```

**Arguments:**

*   `--mode`: Must be `listener`.
*   `--port` (optional): The UDP port to listen for incoming beacon messages. Default: `8080`.
*   `--key` (optional): The shared encryption key for the XOR cipher. Must match the broadcaster's key. Default: `apocalypsai`.

## Example Workflow

1.  **Start a listener on one terminal:**
    ```bash
    ./beacon-broadcast --mode listener --port 8081 --key "mysecretkey"
    ```

2.  **Start a broadcaster on another terminal (or another machine):**
    ```bash
    ./beacon-broadcast --mode broadcaster --port 8080 --interval 2s --key "mysecretkey" --targets "127.0.0.1:8081"
    ```

You should see the listener terminal receiving and decrypting messages every 2 seconds.

## Development

### Running Tests

To run the automated tests, use the Go test command:

```bash
go test ./src/...
```

Tests are designed to be deterministic and offline, simulating network interactions using local UDP ports and capturing output for verification.

### Encryption Details

The XOR cipher used is extremely basic. It's suitable for demonstrating the concept of encrypted communication in a whimsical context but should **not** be used for any real-world security-sensitive applications. The key is simply XORed byte-by-byte with the message, wrapping the key if it's shorter than the message.
