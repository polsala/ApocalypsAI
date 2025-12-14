Nightly Quick Ping

A concurrent TCP ping utility that checks reachability of hosts and ports, reporting latency and status in JSON.

Usage:
  go run src/main.go -hosts=example.com:80,localhost:8080 -timeout=2

Flags:
  -hosts   Comma-separated list of host:port pairs to ping. (required)
  -timeout Timeout in seconds for each ping. Default 2.

Output:
JSON array of ping results, e.g.:

[
  {"host":"example.com","port":80,"success":true,"latency":"1.23ms"},
  {"host":"localhost","port":8080,"success":false,"error":"connection refused"}
]

Testing:
Run `go test ./...` to execute unit tests.
