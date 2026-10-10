# nightly-quote-broadcast

A whimsical Go utility that can act as a TCP server broadcasting a random quote to each connecting client, or as a client that fetches and displays the quote. Perfect for adding a touch of post‑apocalyptic inspiration to your terminal.

## Installation

```sh
go build -o quote-broadcast ./src/main.go
```

## Usage

### Server

```sh
./quote-broadcast server -port 9090
```

Starts a TCP server on port 9090. Each client that connects receives a random quote and the connection is closed.

### Client

```sh
./quote-broadcast client -addr localhost:9090
```

Connects to the server, prints the received quote, and exits.

## How it works

The server spawns a new goroutine for each incoming connection, selects a quote from an embedded list using a deterministic round‑robin counter, writes it to the socket, and closes the connection. The client simply reads until EOF and prints the data.

## Testing

Run the test suite with:

```sh
go test ./...
```
