nightly-chronos-courier
=======================

A whimsical-yet-useful Go-based concurrent network service that acts as a 'Temporal Message Relay'. Clients can send messages to the courier, optionally specifying a delay. The courier will then deliver these messages to *all* currently connected clients once their designated delivery time arrives.

It's like a post office for messages that haven't quite happened yet, perfect for simulating future events, delayed notifications, or just adding a touch of temporal mischief to your communications.

## Features

*   **Concurrent Handling**: Manages multiple client connections simultaneously using Go's goroutines.
*   **Delayed Delivery**: Messages can be prefixed with `DELAY=<duration>:` (e.g., `DELAY=5s:`) to schedule their delivery in the future.
*   **Broadcast**: All delivered messages are sent to every active client connection.
*   **Simple Protocol**: Line-delimited messages over TCP.

## Usage

### 1. Build the Server

Navigate to the `src` directory and build the server:

```bash
cd nightly-chronos-courier/src
go build -o chronos-courier .
```

### 2. Run the Server

Execute the built server. By default, it listens on `localhost:8080`. You can specify a different port using the `-port` flag.

```bash
./chronos-courier -port 8081
```

### 3. Build the Client (Optional, for testing/demonstration)

Navigate to the `src/client` directory and build the client:

```bash
cd nightly-chronos-courier/src/client
go build -o chronos-client .
```

### 4. Run the Client

Execute the client. It will connect to the server (default `localhost:8080`) and send a few example messages, then listen for incoming messages.

```bash
./chronos-client -serverAddr localhost:8081
```

### 5. Interact Manually (e.g., with `netcat`)

You can also connect to the server using `netcat` or `telnet`:

```bash
netcat localhost 8080
```

Once connected, you can send messages:

*   **Immediate Message**: `Hello, present!
`
*   **Delayed Message**: `DELAY=3s:Greetings from 3 seconds in the future!
`
*   **Another Delayed Message**: `DELAY=10s:The prophecy foretells this message.
`

Remember to press Enter after each message to send the newline character.

## Message Format

Messages should be terminated by a newline character (`\n`).

To specify a delay, prefix your message with `DELAY=<duration>:`.

`<duration>` can be any valid Go duration string (e.g., `1s`, `500ms`, `1m30s`).

Examples:

```
Hello, immediate world!

DELAY=5s:This message will arrive in 5 seconds.

DELAY=1m:A minute from now, you'll see this.
```

## Development

### Running Tests

Navigate to the `tests` directory and run the Go tests:

```bash
cd nightly-chronos-courier/tests
go test -v .
```

### Project Structure

```
nightly-chronos-courier/
├── README.md
├── src/
│   ├── main.go         # Chronos Courier Server implementation
│   └── client/
│       └── main.go     # Example client for testing
└── tests/
    └── main_test.go    # Unit and integration tests for the server
```
