# nightly-ping-party

A whimsical concurrent ping utility that checks the latency of multiple hosts (or IPs) by attempting TCP connections. It runs each check in parallel and prints a JSON summary of reachable hosts with their round‑trip times.

## Usage

```sh
go run ./src/main.go host1.com 8.8.8.8 example.org
```

Or pipe a list of hosts (one per line) via stdin:

```sh
cat hosts.txt | go run ./src/main.go
```

## Output

```json
{
  "results": [
    {"host":"host1.com","latency_ms":23.5,"error":null},
    {"host":"8.8.8.8","latency_ms":12.1,"error":null},
    {"host":"example.org","latency_ms":null,"error":"connect timeout"}
  ]
}
```

## Options

- `-timeout` (default 2s) – maximum time to wait for each connection.

## License

MIT
