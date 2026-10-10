# Nightly Starlight Signal Relay

A whimsical Go-based network utility that simulates the vast distances of space by introducing a configurable 'starlight delay' to incoming messages. It acts as a simple TCP server, receiving messages from clients, holding them in a cosmic buffer for a specified duration, and then 'relaying' them to standard output with a thematic log message.

This utility showcases Go's concurrency model using goroutines and channels to handle multiple incoming messages simultaneously, each undergoing its own temporal journey.

## Features

*   **Concurrent Message Handling**: Each incoming message is processed in its own goroutine.
*   **Configurable Starlight Delay**: Set the delay duration via a command-line flag.
*   **Simple TCP Server**: Easy to interact with using `netcat` or any TCP client.
*   **Thematic Logging**: Messages are logged with timestamps indicating reception and relay times, along with the simulated delay.

## Build Instructions

To build the `nightly-starlight-signal-relay` executable, navigate to the `src` directory and run:

```bash
go build -o ../bin/starlight-relay main.go
```

This will create an executable named `starlight-relay` in the `bin` directory.

## Run Instructions

Run the utility from the project root. By default, it listens on port `8080` with a 5-second delay.

```bash
./bin/starlight-relay
```

### Options:

*   `-port <number>`: Specify the listening port (default: `8080`).
*   `-delay <duration>`: Specify the starlight delay (e.g., `5s`, `1m30s`, `2h`). Default: `5s`.

Example with custom port and delay:

```bash
./bin/starlight-relay -port 9000 -delay 10s
```

### Example Usage (using `netcat`):

1.  Start the relay:
    ```bash
    ./bin/starlight-relay -port 8080 -delay 3s
    ```

2.  In another terminal, send a message:
    ```bash
    echo "Hello, distant star!" | nc localhost 8080
    ```

    You should see the message appear in the relay's terminal after approximately 3 seconds:
    ```
    [2023-10-27 22:00:03] Starlight Relay: Message received at 2023-10-27 22:00:00, traversing cosmic dust for 3s... Relayed at 2023-10-27 22:00:03: 'Hello, distant star!'
    ```

## Test Instructions

To run the automated tests, navigate to the `tests` directory and execute:

```bash
go test -v .
```

The tests are designed to be deterministic and do not rely on actual network connections or real-time delays, using mocks for `net.Conn`, `time.Sleep`, and `time.Now`.
