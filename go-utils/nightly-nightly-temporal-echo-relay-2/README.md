# Nightly Temporal Echo Relay

A whimsical-yet-useful Go TCP server designed to simulate network latency and message propagation by introducing a 'temporal echo' delay before broadcasting messages.

## Purpose

This utility acts as a simple TCP relay. Clients connect to it, send messages, and the server holds these messages for a randomized duration (the 'temporal echo'). After this delay, the message is broadcasted to *all* currently connected clients, including the original sender, with a whimsical prefix indicating its temporal journey.

It's useful for:
- **Simulating Network Latency**: Test how your applications behave under varying network delays.
- **Testing Broadcast Systems**: Verify message distribution in a multi-client environment.
- **Debugging Asynchronous Flows**: Observe message ordering and timing in a controlled, delayed setting.
- **Just for Fun**: A quirky chat relay with a temporal twist!

## Features

- **TCP Server**: Listens for incoming client connections.
- **Randomized Echo Delay**: Messages are delayed between 1 and 5 seconds (configurable).
- **Broadcast**: Echoed messages are sent to all active clients.
- **Temporal Prefix**: Each echoed message is prefixed with `[Temporal Echo from <origin_address>]`.

## Installation

1.  **Clone the repository** (or navigate to the `go-utils/nightly-temporal-echo-relay` directory).
2.  **Build the executable**:
    ```bash
    cd go-utils/nightly-temporal-echo-relay/src
    go build -o ../bin/temporal-echo-relay .
    ```

## Usage

1.  **Start the server**:
    ```bash
    ./bin/temporal-echo-relay
    ```
    The server will start listening on `localhost:8080` by default.

2.  **Connect clients**: You can use `netcat` (or `nc`) or any TCP client to connect.
    ```bash
    # Open a terminal for Client 1
    nc localhost 8080

    # Open another terminal for Client 2
    nc localhost 8080
    ```

3.  **Send messages**: Type a message in one client's terminal and press Enter. After a short, random delay, all connected clients (including the sender) will receive the echoed message.

    **Example interaction (Client 1 sends, both receive after delay):**

    **Client 1 Terminal:**
    ```
    Hello, future!
    ```

    **Client 1 & Client 2 Terminals (after delay):**
    ```
    [Temporal Echo from 127.0.0.1:<client1_port>] Hello, future!
    ```

## Configuration

The server currently uses hardcoded values for the port (`8080`), minimum echo delay (`1s`), and maximum echo delay (`5s`). For more advanced use cases, these can be modified directly in `src/main.go`.

## Development & Testing

To run the automated tests:

```bash
cd go-utils/nightly-temporal-echo-relay/tests
go test -v .
```

The tests use mock network connections and a mocked `time.Sleep` function to ensure determinism and fast execution without actual network I/O or delays.
