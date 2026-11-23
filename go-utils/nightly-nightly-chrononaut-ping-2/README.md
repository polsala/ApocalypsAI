# nightly-chrononaut-ping

A whimsical concurrent ping utility written in Go. It "pings" a list of hosts concurrently, measuring TCP connection latency, and reports results in JSON. Useful for quick health checks of multiple endpoints.

## Usage

```sh
go run src/main.go -hosts=example.com,google.com -count=3
```

### Flags

- `-hosts` (comma‑separated list of hostnames or IPs)
- `-count` number of ping attempts per host (default 1)
- `-timeout` per‑attempt timeout in seconds (default 2)

The program prints a JSON object with each host, average latency in milliseconds, and a success flag.

## Example Output

```json
{
  "results": [
    {"host":"example.com","avg_latency_ms":23.5,"success":true},
    {"host":"nonexistent.invalid","avg_latency_ms":0,"success":false}
  ]
}
```

## Testing

Run `go test ./...` to execute deterministic unit tests that mock network latency.
