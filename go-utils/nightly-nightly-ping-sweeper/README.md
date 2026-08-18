# nightly-ping-sweeper

A whimsical concurrent ping sweeper written in Go. It checks a list of hostnames/IPs for TCP reachability on port 80 using goroutines and reports which hosts are up.

## Build

```sh
go build -o ping-sweeper ./src
```

## Usage

```sh
./ping-sweeper host1.com 192.168.1.1 example.org
```

The program will probe each host concurrently (default 10 workers) and print reachable hosts.

## How it works

- Uses a worker pool limited by a semaphore channel.
- Each worker attempts a TCP connection to port 80 with a 2‑second timeout.
- Results are collected and printed in the order of input.

## Testing

Run `go test ./tests` to execute deterministic unit tests that mock the network calls.
