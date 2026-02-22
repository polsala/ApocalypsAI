# Nightly Temporal Whisper Relay

## Overview

The `nightly-temporal-whisper-relay` is a whimsical-yet-useful Go-based network utility that acts as a message relay with a temporal twist. It listens for incoming messages on a specified TCP port. When a message is received from a client, the relay holds onto it for a randomized duration (simulating a 'temporal delay') before broadcasting it to *all other* connected clients. The original sender does not receive their own message back.

This utility can be used for:

*   **Simulating network latency**: Test how your applications behave under varying message delivery delays.
*   **Asynchronous system testing**: Verify message processing in systems that expect delayed or out-of-order delivery.
*   **Whimsical chat room**: Create a unique chat experience where messages arrive as 'whispers from the past'.
*   **Load testing**: Simulate multiple concurrent clients sending and receiving delayed messages.

## Features

*   **Concurrent Client Handling**: Efficiently manages multiple client connections using Go goroutines.
*   **Configurable Delay**: Set minimum and maximum delay ranges for message broadcasting.
*   **Broadcast Mechanism**: Messages are relayed to all clients *except* the original sender.
*   **Lightweight**: Built with Go for high performance and low resource consumption.

## Installation

To build the `nightly-temporal-whisper-relay`:

1.  Ensure you have Go (version 1.16 or higher) installed.
2.  Navigate to the utility's directory:
    ```bash
    cd go-utils/nightly-temporal-whisper-relay
    ```
3.  Build the executable:
    ```bash
    go build -o temporal-whisper-relay src/main.go
    ```

This will create an executable named `temporal-whisper-relay` in the current directory.

## Usage

Run the relay server:

```bash
./temporal-whisper-relay --port 8080 --min-delay 100ms --max-delay 2s
```

### Command-line Flags:

*   `--port <port>`: The TCP port the relay will listen on. (Default: `8080`)
*   `--min-delay <duration>`: The minimum randomized delay before broadcasting a message. (Default: `100ms`)
*   `--max-delay <duration>`: The maximum randomized delay before broadcasting a message. (Default: `500ms`)

**Example**: To run on port 9000 with delays between 500 milliseconds and 3 seconds:

```bash
./temporal-whisper-relay --port 9000 --min-delay 500ms --max-delay 3s
```

### Connecting Clients

You can connect to the relay using `netcat` (nc) or any TCP client:

**Client 1 (sending messages):**

```bash
nc localhost 8080
```

Type your message and press Enter. It will be sent to the relay.

**Client 2 (receiving echoes):**

Open another terminal and connect:

```bash
nc localhost 8080
```

Client 2 will receive messages sent by Client 1 (and any other clients) after a randomized delay, prefixed with "Echo from the past...".

**Example Interaction:**

*   **Client 1:** `Hello, is anyone there?`
*   *(After a random delay, say 1.2s)*
*   **Client 2:** `Echo from the past (127.0.0.1:XXXXX): Hello, is anyone there?`

## Development

### Running Tests

To run the automated tests for the utility:

```bash
cd go-utils/nightly-temporal-whisper-relay
go test ./tests/...
```

Tests use `net.Pipe()` to create in-memory network connections, ensuring determinism and isolation from actual network conditions.
