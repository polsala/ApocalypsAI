# Nightly Temporal Echo Chamber

## Overview

The `nightly-temporal-echo-chamber` is a whimsical Go-based network utility that acts as a distributed echo chamber. It listens for incoming TCP connections, accepts messages from clients, and then broadcasts those messages back to *all* currently connected clients after a configurable, randomized delay. To add a touch of temporal anomaly, messages can optionally be distorted (reversed) before being echoed.

This utility is useful for:
-   **Testing network communication**: Simulate message propagation delays and broadcast scenarios.
-   **Distributed system debugging**: Observe how messages are echoed across multiple client connections.
-   **Just for fun**: Create a chaotic chat room where messages bounce around with unpredictable timing and minor distortions.

## Features

-   **Concurrent Client Handling**: Manages multiple client connections efficiently using Go goroutines.
-   **Randomized Delay**: Messages are echoed after a delay within a specified range, simulating temporal anomalies.
-   **Message Distortion**: Optionally reverses the message string before echoing it.
-   **Configurable**: Port, delay range, and distortion can be set via command-line flags.

## Installation

1.  **Prerequisites**: Ensure Go (1.16 or higher) is installed on your system.
2.  **Clone the repository** (if not already done):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-temporal-echo-chamber
    ```
3.  **Build the utility**:
    ```bash
    go build -o temporal-echo-chamber src/main.go
    ```

## Usage

Run the echo chamber server:

```bash
./temporal-echo-chamber [flags]
```

### Command-line Flags:

-   `-port <number>`: The port the server will listen on. (Default: `8080`)
-   `-min-delay <duration>`: Minimum delay before echoing a message (e.g., `1s`, `500ms`). (Default: `500ms`)
-   `-max-delay <duration>`: Maximum delay before echoing a message (e.g., `5s`, `2s`). (Default: `2s`)
-   `-distort`: Enable message distortion (reverses the message string). (Default: `false`)

### Examples:

1.  **Start with default settings (port 8080, 500ms-2s delay, no distortion)**:
    ```bash
    ./temporal-echo-chamber
    ```

2.  **Start on port 9000 with a longer delay and distortion enabled**:
    ```bash
    ./temporal-echo-chamber -port 9000 -min-delay 1s -max-delay 5s -distort
    ```

### Connecting Clients:

You can connect to the echo chamber using `netcat` (nc) or any TCP client.

**Client 1 (in one terminal):**
```bash
nc localhost 8080
```

**Client 2 (in another terminal):**
```bash
nc localhost 8080
```

Now, type messages in either client. After a short, randomized delay, the message (possibly distorted) will appear in *both* client terminals.

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
go test ./tests/...
```

Tests are designed to be deterministic and offline, using mock network connections to simulate client interactions without actual network I/O.
