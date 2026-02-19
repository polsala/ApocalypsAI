# nightly-udp-echo

A whimsical concurrent UDP echo server and client for measuring round‑trip latency on the local network.

## Overview

`nightly-udp-echo` can run in two modes:

- **server** – Listens on a UDP port and echoes back any received packet.
- **client** – Sends a message to a server and reports the round‑trip time.

## Installation

```sh
go build -o nightly-udp-echo ./src
```

## Usage

### Server

```sh
./nightly-udp-echo -mode=server -addr=0.0.0.0:9000
```

### Client

```sh
./nightly-udp-echo -mode=client -addr=127.0.0.1:9000 -msg="hello" -count=5
```

The client will send the message `count` times and print each RTT.

## License

MIT
