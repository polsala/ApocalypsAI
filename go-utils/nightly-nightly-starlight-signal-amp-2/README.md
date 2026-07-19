# Nightly Starlight Signal Amplifier

## Overview

The `nightly-starlight-signal-ampli` is a whimsical-yet-useful Go-based concurrent network utility designed to amplify messages across the ApocalypsAI community. When a message is received by the amplifier, it's imbued with a unique "cosmic signature" and a precise timestamp, then broadcast to all other connected clients. Think of it as a cosmic switchboard for your whispers and signals across the digital wasteland.

This utility showcases Go's powerful concurrency features (goroutines and channels) and its `net` package for building robust network services.

## Features

*   **Concurrent Client Handling**: Efficiently manages multiple simultaneous client connections.
*   **Message Amplification**: Automatically adds a timestamp and a unique cosmic signature (UUID) to every incoming message.
*   **Broadcast Functionality**: Relays amplified messages to all currently connected clients.
*   **Simple TCP Protocol**: Easy to interact with using standard `netcat` or custom client scripts.

## Installation

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed on your system.

2.  **Clone the repository** (if not already done):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-starlight-signal-ampli
    ```

3.  **Build the executable**:
    ```bash
    go mod init nightly-starlight-signal-ampli
    go get github.com/google/uuid
    go build -o starlight-amplifier src/main.go
    ```

## Usage

To start the Starlight Signal Amplifier server:

```bash
./starlight-amplifier --port 8080
```

(Replace `8080` with your desired port. Default is `8080` if not specified.)

### Connecting Clients

You can connect to the server using `netcat` or any TCP client:

**Client 1:**
```bash
# Open a terminal for Client 1
netcat localhost 8080
```

**Client 2:**
```bash
# Open another terminal for Client 2
netcat localhost 8080
```

Now, type messages into either `netcat` terminal. You will see the amplified message (with timestamp and cosmic signature) appear in *both* terminals.

Example interaction:

**Client 1 sends:**
```
Hello, cosmic void!
```

**Both Client 1 and Client 2 receive (example output):**
```
[2023-10-27 10:30:00 UTC] [Cosmic-Sig: 8a7b6c5d-4e3f-2a1b-0c9d-8e7f6a5b4c3d] Hello, cosmic void!
```

## Development & Testing

To run the automated tests:

```bash
cd go-utils/nightly-starlight-signal-ampli
go test ./tests/...
```

Tests are self-contained and use `net.Pipe()` to simulate network connections, ensuring determinism and offline execution.
