# nightly-void-ping

A whimsical Go utility that "pings" a list of hosts concurrently and reports deterministic fake latency values. Useful for testing scripts that expect ping output without needing network access.

## Usage

```sh
go run ./src/main.go host1.example.com host2.local
```

Outputs a JSON array:

```json
[
  {"host":"host1.example.com","latency_ms":42},
  {"host":"host2.local","latency_ms":17}
]
```

## How it works

The tool hashes each hostname (by summing its byte values) and derives a latency between 1‑100 ms, ensuring the same host always yields the same value. No real network traffic is sent.

## Building

```sh
go build -o void-ping ./src/main.go
```

## Testing

```sh
go test ./tests
```
