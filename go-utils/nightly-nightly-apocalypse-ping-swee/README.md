# Nightly Apocalypse Ping Sweeper

A whimsical CLI tool that concurrently checks a list of IP addresses (or hostnames) for reachability on TCP port 80, reporting which ones are alive. Useful for network admins in a post‑apocalyptic setting to locate surviving servers.

## Installation

```sh
go build -o ping-sweeper ./src/main.go
```

## Usage

```sh
./ping-sweeper 192.0.2.1 example.com 203.0.113.5
```

Outputs:

```
192.0.2.1: alive
example.com: dead
203.0.113.5: alive
```

## How it works

- Spawns a goroutine per target.
- Uses a 2‑second timeout for each TCP dial to port 80.
- Collects results via channel and prints in the order the hosts were supplied.

## Testing

Run `go test ./...` to execute deterministic unit tests that mock network calls.
