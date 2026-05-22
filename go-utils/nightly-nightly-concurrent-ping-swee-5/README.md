Nightly Concurrent Ping Sweeper

Overview:
A lightweight Go tool that concurrently pings (via TCP connect) a list of host:port pairs and reports the latency in milliseconds. Useful for quick health‑checks of services in a micro‑service environment.

Build & Run:

    go build -o ping-sweeper ./src/main.go
    ./ping-sweeper host1:80 host2:443 ...

Or run directly with go run:

    go run ./src/main.go host1:80 host2:443

The program prints a pretty‑printed JSON array where each element contains the host, measured latency (ms), and an error field if the connection failed.

Example output:

    [
      {
        "host": "example.com:80",
        "latency_ms": 23.4
      },
      {
        "host": "unreachable.local:1234",
        "error": "dial tcp 192.0.2.1:1234: connect: connection refused"
      }
    ]

The concurrency level is capped at 10 simultaneous connections and each attempt times out after 2 seconds.
