Nightly Echo Multitool
=======================

Overview
--------
A tiny Go utility that runs two services concurrently:

1. **TCP Echo Server** – Listens for TCP connections, echoes each line back to the client, and counts connections.
2. **HTTP Stats Server** – Exposes `/stats` which returns the total number of TCP connections handled.

Both services run in the background and the program blocks forever, making it suitable for quick demos or as a building block for larger systems.

Build & Run
-----------
```bash
# Build the binary
go build -o echo-multitool src/main.go

# Run (default ports: TCP 9000, HTTP 9001)
./echo-multitool
```

Custom ports can be set by editing the `tcpAddr` and `httpAddr` variables in `src/main.go` before building.

Testing
-------
Run the automated test suite with:
```bash
go test ./tests
```
The test starts the servers on random free ports, verifies that a line sent to the TCP server is echoed back, and checks that the HTTP `/stats` endpoint reports exactly one connection.

License
-------
MIT – see LICENSE file in the repository root.
