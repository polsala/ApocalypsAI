# Nightly Chronal Comm Delay

## Overview

The `nightly-chronal-comm-delay` is a whimsical-yet-useful Go-based TCP server that introduces a configurable, randomized delay before relaying received messages to *all* connected clients. It simulates a "chronal ripple" or a time-distorted communication channel, making it ideal for:

*   **Network Latency Simulation**: Test how client applications behave under varying, unpredictable network delays.
*   **Distributed System Resilience Testing**: Evaluate the robustness of systems that need to handle out-of-order or delayed messages.
*   **Whimsical Chat**: Create a fun, echo-chamber-like chat experience where messages arrive with a temporal twist.

## Features

*   **Concurrent Client Handling**: Manages multiple client connections simultaneously.
*   **Configurable Delay Range**: Set minimum and maximum delay times (in milliseconds) via command-line arguments.
*   **Randomized Delays**: Each message experiences a unique delay within the specified range.
*   **Broadcast Functionality**: Every message received is broadcast to all active clients after its delay.
*   **Graceful Shutdown**: Handles `SIGINT` (Ctrl+C) to shut down cleanly.

## Installation

To install the utility, you need Go (version 1.16 or higher) installed on your system.

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-chronal-comm-delay
    ```

2.  **Build the executable:**
    ```bash
    go build -o chronal-comm-delay src/main.go
    ```

    This will create an executable named `chronal-comm-delay` in the current directory.

## Usage

Run the server from your terminal:

```bash
./chronal-comm-delay [options]
```

### Options

*   `-port <number>`: The TCP port to listen on. (Default: `8080`)
*   `-min-delay <ms>`: Minimum delay in milliseconds before broadcasting a message. (Default: `1000`)
*   `-max-delay <ms>`: Maximum delay in milliseconds before broadcasting a message. (Default: `5000`)

### Examples

1.  **Run with default settings (port 8080, 1-5 second delay):**
    ```bash
    ./chronal-comm-delay
    ```

2.  **Run on port 9000 with a shorter, tighter delay (0.5-1.5 seconds):**
    ```bash
    ./chronal-comm-delay -port 9000 -min-delay 500 -max-delay 1500
    ```

### Connecting Clients

You can connect to the server using `netcat` (nc) or any TCP client.

**Terminal 1 (Run Server):**
```bash
./chronal-comm-delay -port 8080 -min-delay 1000 -max-delay 2000
```

**Terminal 2 (Client 1):**
```bash
nc localhost 8080
Hello from Client 1!
```

**Terminal 3 (Client 2):**
```bash
nc localhost 8080
Greetings from Client 2!
```

After Client 1 sends "Hello from Client 1!", both Client 1 and Client 2 will receive that message after a random delay between 1 and 2 seconds. The same applies when Client 2 sends its message.

## Development

### Running Tests

To run the automated tests, navigate to the utility's directory and execute:

```bash
go test ./src -v
```

The tests use a mocked delay generator to ensure deterministic and fast execution, verifying the server's core logic without actual time delays.
