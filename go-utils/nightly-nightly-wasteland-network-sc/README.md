# nightly-wasteland-network-scout

A whimsical concurrent network scanner written in Go. It crawls a CIDR subnet, probes a list of TCP ports, and assigns each discovered host a post‑apocalyptic nickname (e.g., “Wasteland Wanderer”, “Radiated Raider”). Perfect for community drills, LAN parties, or just for fun.

## Features

- Fully concurrent scanning using goroutines.
- Configurable CIDR range and port list via command‑line flags.
- Deterministic output with whimsical host nicknames.
- Zero external dependencies – just the Go standard library.

## Installation

```sh
go build -o wasteland-scout ./src/main.go
```

## Usage

```sh
./wasteland-scout -cidr=192.168.1.0/24 -ports=22,80,443
```

Example output:

```
Host 192.168.1.5 (Radiated Raider) open ports: 22, 80
Host 192.168.1.12 (Wasteland Wanderer) open ports: 443
```

## Testing

```sh
go test ./tests/...
```

The test suite uses a mock dialer to simulate open/closed ports, ensuring deterministic offline execution.
