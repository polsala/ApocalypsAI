# Apocalypse Ping Party

**nightly-apocalypse-ping-party** is a tiny Go utility that concurrently "pings" a list of hosts using TCP connections. It measures how long it takes to establish a connection (or times out) and prints a fun, apocalypse‑themed status line for each host.

## Features

- Accepts a list of host:port pairs via command‑line arguments.
- Performs all checks concurrently using goroutines.
- Reports latency in milliseconds.
- Prints a random apocalypse‑style message (e.g., "The skies burn", "Ravens gather") for each host.
- Zero external dependencies – just the Go standard library.

## Installation

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd go-utils/nightly-apocalypse-ping-party
go build -o apoc-ping ./src/main.go
```

## Usage

```bash
# Basic usage – provide hosts as arguments
./apoc-ping example.com:80 192.0.2.1:22 localhost:8080
```

Output example:

```
[✔] example.com:80 – 23ms – The skies burn.
[✖] 192.0.2.1:22 – unreachable – Ravens gather.
[✔] localhost:8080 – 1ms – Ashes rise.
```

## How it works

The program uses `net.DialTimeout` to attempt a TCP connection to each target. The duration of a successful connection is recorded; failures are reported as *unreachable*. A small slice of apocalypse‑themed phrases is shuffled, and each host gets a random phrase.

## Testing

Run the unit tests with:

```bash
go test ./tests
```

The tests spin up a temporary TCP server to verify both reachable and unreachable scenarios.
