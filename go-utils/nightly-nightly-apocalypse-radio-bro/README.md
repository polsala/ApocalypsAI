# Apocalypse Radio Broadcast

**nightly‑apocalypse‑radio‑broadcast** is a tiny Go utility that simulates a “post‑apocalyptic radio” station.  It listens on a TCP port and, for each incoming connection, streams a series of short, randomly‑selected messages (including static) with a short pause between them.  The tool is deliberately whimsical but can be handy for testing client code that consumes streaming text data.

## Features

- Concurrent handling of multiple clients (each connection runs in its own goroutine).
- Randomized message selection using a seeded `math/rand.Rand` – deterministic in tests.
- Small, self‑contained binary – no external dependencies beyond the Go standard library.

## Installation

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-apocalypse-radio-broadcast
go build -o radio-broadcast ./src/main.go
```

## Usage

```bash
# Run the server on the default port 8080
./radio-broadcast

# Or specify a custom port
./radio-broadcast -port 9000
```

Clients can connect with `nc`, `telnet`, or any TCP client library:

```bash
nc localhost 8080
```

You will see a stream of messages such as:

```
... static ...
This is the last broadcast from the wasteland.
Do you hear the wind? It carries whispers of the old world.
```

## Testing

The utility includes a deterministic unit test that uses a fixed random seed and a `net.Pipe` to avoid real network traffic.  Run the tests with:

```bash
go test ./tests
```

## License

MIT – see the root `LICENSE` file.
