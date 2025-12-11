# Nightly Wasteland Quote Broadcaster

A tiny Go utility that runs a UDP server which, on every request, replies with a random post‑apocalyptic survival quote.  A companion client can be used to fetch a quote from the server.

## Features
- **Concurrent**: Handles multiple UDP requests simultaneously.
- **Deterministic for testing**: The random source can be seeded, making unit tests reliable.
- **Zero external dependencies** – only the Go standard library.

## Install
```bash
# Clone the repository (or copy the files into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-wasteland-quote-broadcaster

# Build the binary
go build -o quote-broadcaster ./src/main.go
```

## Usage
### Run the server
```bash
./quote-broadcaster -mode=server -port=9000
```
The server will listen on UDP port `9000` and reply to any incoming packet with a random quote.

### Run the client
```bash
./quote-broadcaster -mode=client -address=localhost:9000
```
The client sends a single empty packet to the server and prints the received quote.

## Testing
```bash
go test ./tests
```
All tests are deterministic and run offline.

## License
MIT © ApocalypsAI
