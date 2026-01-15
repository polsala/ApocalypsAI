Nightly Portal Ping
A whimsical concurrent TCP ping utility written in Go. It measures round‑trip latency to one or more host:port endpoints in parallel, useful for quick network health checks in post‑apocalyptic comms.

Usage:
  portal-ping <host1:port> [host2:port] ...

Example:
  portal-ping 8.8.8.8:53 1.1.1.1:53

The tool will print each host with latency in milliseconds or "unreachable" if the connection fails.

Running tests:
  go test ./...
