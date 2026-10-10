# Wasteland Ping Aggregator

A whimsical concurrent ping utility written in Go. It attempts TCP connections to a list of hosts, measures latency, and presents the results in a post‑apocalyptic poetic style.

## Build

```sh
go build -o wasteland-ping ./src
```

## Usage

```sh
./wasteland-ping host1.com host2.com 192.0.2.1
```

If no hosts are provided, it pings a default set of well‑known sites.

## How it works

- Launches a goroutine per host.
- Measures time to establish a TCP connection (default port 80) with a 2‑second timeout.
- Sorts results by latency.
- Prints a whimsical line for each host.

## Testing

```sh
go test ./...
```
