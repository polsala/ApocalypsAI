# Portal Ping

A whimsical concurrent network latency checker written in Go.
It dials multiple hosts in parallel (default TCP port) and reports latency, helping you test the fabric of reality.

## Build

```sh
go build -o portal-ping ./src
```

## Usage

```sh
./portal-ping host1:80,host2:443,example.com:22
```

The tool prints a table with latency and status for each host.

## Testing

```sh
go test ./tests
```

## How it works

- Parses a commaâseparated list of host:port.
- Launches a goroutine per host using `net.DialTimeout`.
- Collects results via a `sync.WaitGroup`.
- Displays a formatted table.

Enjoy probing the multiverse, one TCP handshake at a time!
