# Nightly Starlight Signal Amplifier

## Overview

The `nightly-starlight-signal-amp` is a whimsical Go-based network utility designed to detect and amplify specific 'starlight signals' across a network. When a client sends a predefined signal (e.g., `STARLIGHT_PING`), the amplifier detects it and broadcasts a randomly selected, whimsical, and 'amplified' message to all currently connected clients.

This utility is perfect for adding a touch of cosmic wonder to your network monitoring, or simply for a fun, distributed messaging system that reacts to specific triggers.

## Features

*   **Concurrent Client Handling**: Manages multiple client connections simultaneously using Go's goroutines.
*   **Signal Detection**: Listens for a specific keyword (`STARLIGHT_PING`) in incoming messages.
*   **Whimsical Amplification**: Upon signal detection, broadcasts a random, pre-defined whimsical message to all connected clients.
*   **Simple TCP Protocol**: Easy to interact with using standard `netcat` or custom client applications.
*   **Graceful Shutdown**: Handles `Ctrl+C` (SIGINT/SIGTERM) to shut down cleanly.

## How to Run

1.  **Prerequisites**: Ensure you have Go (version 1.16 or higher) installed.

2.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-starlight-signal-amp
    ```

3.  **Build the executable**:
    ```bash
    go build -o starlight-amp src/main.go
    ```

4.  **Run the server**:
    ```bash
    ./starlight-amp
    ```
    By default, the server will listen on port `8080`.

## How to Use (Client Interaction)

You can connect to the server using `netcat` or any TCP client.

1.  **Connect to the server** (in a new terminal):
    ```bash
    nc localhost 8080
    ```

2.  **Send a non-signal message**: The server will echo it back.
    ```
    Hello, cosmic void!
    ```
    You should see: `Starlight Amplifier received: Hello, cosmic void!`

3.  **Send the 'starlight signal'**: The server will broadcast an amplified message to all connected clients.
    ```
    STARLIGHT_PING
    ```
    All connected clients (including the one that sent the signal) will receive a message like:
    `✨ AMPLIFIED SIGNAL DETECTED! ✨ The cosmos hums with your brilliance! (from 127.0.0.1:54321)`

    Try opening multiple `netcat` sessions and observe the broadcast!

## Automated Tests

To run the tests for this utility:

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-starlight-signal-amp
    ```

2.  **Run the tests**:
    ```bash
    go test ./tests/main_test.go ./src/main.go
    ```

The tests use mock network connections to ensure determinism and isolation from actual network operations.
