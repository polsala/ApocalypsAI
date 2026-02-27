# Nightly Chronal Chatterbox

## Summary

The Nightly Chronal Chatterbox is a whimsical-yet-useful Go-based network utility that simulates temporal distortions in communication. It listens on a specified TCP port, receives incoming messages, and then "echoes" them back to the sender after a randomized delay (between 1 and 6 seconds). Each echoed message is prefixed to indicate its temporal journey.

This tool is perfect for:
*   **Testing Asynchronous Systems**: Simulate network latency and delayed responses in your local development environment without complex network configurations.
*   **Chaos Engineering Lite**: Introduce controlled, minor delays to observe how your applications handle non-instantaneous feedback.
*   **Learning Go Concurrency**: A practical example of Go's `goroutine` and `channel` patterns for handling multiple concurrent network connections.

## How to Run

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-chronal-chatterbox
    ```

2.  **Build the Go application**:
    ```bash
    go build -o chronal-chatterbox src/main.go
    ```

3.  **Run the server**:
    ```bash
    ./chronal-chatterbox
    # Or specify a port:
    # PORT=9000 ./chronal-chatterbox
    ```
    By default, it will listen on `localhost:8080`. You'll see output like:
    `Chronal Chatterbox listening on port 8080`

## How to Use

Once the server is running, you can connect to it using `netcat` or any TCP client.

1.  **Open another terminal and connect**:
    ```bash
    nc localhost 8080
    ```

2.  **Type a message and press Enter**:
    ```
    Hello, future self!
    ```

3.  **Wait for the echo**: After a randomized delay, you will receive your message back, prefixed by the Chatterbox:
    ```
    [Echoed from Chronal Chatterbox after 3.45s]: Hello, future self!
    ```

## How to Test

1.  **Navigate to the utility directory**:
    ```bash
    cd go-utils/nightly-chronal-chatterbox
    ```

2.  **Run the Go tests**:
    ```bash
    go test ./tests/...
    ```
    The tests use `net.Pipe()` to simulate network connections in-memory, ensuring deterministic and offline execution without actual network binding.
