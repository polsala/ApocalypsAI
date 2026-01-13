# Nightly Clipboard Telepathy

## Overview

`nightly-clipboard-telepathy` is a playful Go utility that lets you share your clipboard (or any text) across machines on the same local network in real time. It works by broadcasting each line you type (or copy) over UDP and printing any incoming messages from peers.

## Features

- **Zeroâconfiguration**: just run the binary on each machine and it will discover peers via UDP broadcast.
- **Concurrent**: listening and sending run in separate goroutines, so you can type while receiving.
- **Crossâplatform**: works on any OS with Go installed.
- **Whimsical**: think of it as âclipboard telepathyâ for the apocalypse.

## Installation

```bash
# Clone the repository (or copy the generated files)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-clipboard-telepathy

# Build the binary
go build -o clipboard-telepathy src/main.go
```

## Usage

Run the program and start typing. Each line you enter is broadcast to the network. Incoming lines from other machines are printed with a `[remote]` prefix.

```bash
./clipboard-telepathy            # uses default port 9999
./clipboard-telepathy -port 7777 # custom port
```

You can also pipe data into it:

```bash
echo "Secret message" | ./clipboard-telepathy
```

## How It Works

- **Listener**: a UDP socket bound to `0.0.0.0:<port>` receives broadcast packets and prints the payload.
- **Broadcaster**: reads stdin lineâbyâline, trims whitespace, and sends the payload to the broadcast address `255.255.255.255:<port>`.
- **Concurrency**: both components run in separate goroutines and communicate via channels.

## Testing

The utility includes a small test suite that verifies the core encode/decode logic. Run tests with:

```bash
go test ./...
```

## License

MIT License â see the repository root for details.

