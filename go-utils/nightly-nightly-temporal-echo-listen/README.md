# Nightly Temporal Echo Listener

"Listen closely, for the whispers of time carry echoes from beyond the veil."

The `nightly-temporal-echo-listen` is a whimsical yet useful Go-based concurrent TCP server designed to simulate listening for "temporal echoes" – simple text messages sent over a network. It processes each incoming message by assigning a unique echo ID, stamping it with the current time, and logging it to the console.

This utility is excellent for:
- **Testing concurrent systems**: Simulate a message sink that handles multiple incoming connections and messages concurrently.
- **Network debugging**: A simple TCP server to send arbitrary text data to and observe its processing.
- **Educational purposes**: Demonstrate Go's concurrency primitives (`goroutines`, `channels`, `sync.WaitGroup`, `sync.Mutex`).
- **Pure whimsy**: Just because it's fun to imagine listening to temporal echoes!

## Features
- **Concurrent Handling**: Each client connection is handled in its own goroutine.
- **Message Processing**: Assigns a unique ID and timestamp to each received message.
- **Centralized Logging**: Processed echoes are sent to a dedicated logging goroutine via a channel.
- **Graceful Shutdown**: Responds to `SIGINT` (Ctrl+C) and `SIGTERM` for clean termination.

## How to Run

1.  **Prerequisites**:
    *   Go (version 1.16 or higher) installed on your system.

2.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-temporal-echo-listen
    ```

3.  **Build the executable**:
    ```bash
    go build -o temporal-echo-listener src/main.go
    ```

4.  **Run the server**:
    ```bash
    ./temporal-echo-listener
    ```
    By default, the server will listen on port `8080`. You can specify a different port using the `PORT` environment variable:
    ```bash
    PORT=9000 ./temporal-echo-listener
    ```

5.  **Send echoes (messages) to the server**:
    You can use `netcat` (nc) or `telnet` to connect to the server.

    *   **Using `netcat` (recommended)**:
        ```bash
        echo "Hello from the past!" | nc localhost 8080
        echo "A ripple in the fabric of time." | nc localhost 8080
        ```
        For an interactive session:
        ```bash
        nc localhost 8080
        # Type your messages, press Enter after each
        # Press Ctrl+D to close the connection
        ```

    *   **Using `telnet` (if `nc` is not available)**:
        ```bash
        telnet localhost 8080
        # Type your messages, press Enter after each
        # Press Ctrl+] then type 'quit' and Enter to close
        ```

    You will see output similar to this on the server's console:
    ```
    2023/10/27 10:30:00 Temporal Echo Listener started on :8080
    2023/10/27 10:30:05 New temporal conduit opened from 127.0.0.1:54321
    [ECHO 1] 2023-10-27T10:30:05Z from 127.0.0.1:54321: "Hello from the past!"
    [ECHO 2] 2023-10-27T10:30:06Z from 127.0.0.1:54321: "A ripple in the fabric of time."
    2023/10/27 10:30:06 Temporal conduit from 127.0.0.1:54321 closed.
    ```

6.  **Stop the server**:
    Press `Ctrl+C` in the terminal where the server is running.

## How to Test

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-temporal-echo-listen
    ```

2.  **Run the tests**:
    ```bash
    go test ./tests/...
    ```
    This will execute all unit and integration tests, including those that simulate network interactions using `net.Pipe()` for offline, deterministic testing, and full end-to-end tests using ephemeral ports.
