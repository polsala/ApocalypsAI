# nightly-portal-ping-multicast

A whimsical Go utility that concurrently "pings" a list of hosts (via TCP connection) to see which portals to other dimensions are open. It reports latency and success/failure in a tidy table.

## Usage

```sh
go run ./src/main.go host1:port host2:port ...
```

Or build:

```sh
go build -o portal-ping ./src/main.go
./portal-ping host1:port host2:port
```

## Example

```sh
$ ./portal-ping example.com:80 localhost:22 nonexistent:1234
Host                     Status   Latency
example.com:80           open     12ms
localhost:22             open     3ms
nonexistent:1234         closed   -
```

## How it works

- Accepts `host:port` arguments.
- Launches a goroutine per host, attempts a TCP connection with a 2 s timeout.
- Measures elapsed time.
- Collects results via a channel, sorts open hosts by latency, and prints a table.

## Testing

Run `go test ./...` to execute deterministic unit tests that mock network behavior.
