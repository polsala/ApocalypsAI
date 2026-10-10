# nightly-beacon-broadcast

A whimsical-yet-useful Go-based utility for broadcasting short, encrypted messages across a local network, simulating post-apocalyptic communication. This system comprises a simple UDP server that listens for messages and a client that sends them, using a basic XOR cipher for "scrambling" the transmissions.

## Features

*   **UDP-based Communication**: Lightweight and connectionless, suitable for unreliable network conditions.
*   **Simple XOR Encryption**: Messages are scrambled with a fixed key before transmission, adding a layer of "mystery" (not security!).
*   **Concurrent Server**: The server can handle multiple incoming beacon messages simultaneously using Go's goroutines.
*   **Standalone Client**: A command-line client to send messages to the beacon server.

## Classifier

`go-utils`

## How to Build

Navigate to the `nightly-beacon-broadcast` directory.
Ensure you have Go (version 1.16 or higher) installed.

```bash
# Initialize Go module (if not already done, though it should be in the generated structure)
go mod init nightly-beacon-broadcast
go mod tidy # To generate go.sum

# Build the server executable
go build -o bin/beacon-server ./src/server

# Build the client executable
go build -o bin/beacon-client ./src/client
```

This will create `beacon-server` and `beacon-client` executables in a `bin/` directory.

## How to Run

### 1. Start the Beacon Server

Open a terminal and run the server:

```bash
./bin/beacon-server --port 8080
```

The server will start listening on UDP port `8080` (or your specified port) and log incoming messages.

### 2. Send a Beacon Message from a Client

Open another terminal and run the client to send a message:

```bash
./bin/beacon-client --server 127.0.0.1:8080 --message "Alpha team, status report. Over."
```

Replace `127.0.0.1:8080` with the actual IP and port where your server is running, and `"Alpha team, status report. Over."` with your desired message.

You should see the message appear in the server's terminal, decrypted and logged.

## Automated Tests

To run the tests, navigate to the `nightly-beacon-broadcast` directory and execute:

```bash
go test ./tests/...
```

This will run:
*   Unit tests for the XOR cipher (`cipher_test.go`).
*   An integration test that starts a server, sends messages from multiple clients, and verifies that the server correctly receives and decrypts them (`server_client_integration_test.go`).

## Code Structure

```
.
├── README.md
├── go.mod
├── go.sum
├── src/
│   ├── client/
│   │   └── main.go   # Client application entry point
│   ├── server/
│   │   └── main.go   # Server application entry point
│   └── cipher/
│       └── cipher.go # Simple XOR cipher implementation
└── tests/
    ├── cipher_test.go                # Unit tests for the cipher
    └── server_client_integration_test.go # Integration test for server and client
```
