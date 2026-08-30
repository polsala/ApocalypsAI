Nightly Portal Ping Utility

Overview
This tiny Go program pretends to ping a list of hosts. It does not perform real network traffic; instead it generates a deterministic fake latency for each host based on a SHA‑1 hash. The result is a whimsical way to see “ping” times for any set of names without needing network access.

Features
* Concurrent execution – each host is “pinged” in its own goroutine.
* Deterministic latency – the same host always yields the same latency, making tests reliable and offline.
* Simple command‑line interface.

Build & Run
1. Ensure you have Go 1.22 or later installed.
2. Build the binary:
   go build -o portal-ping ./src/main.go
3. Run it with any number of host strings:
   ./portal-ping alpha.example beta.example gamma.example

The program will print lines of the form:
   alpha.example: 73ms
   beta.example: 158ms
   gamma.example: 42ms

Testing
Run the test suite with:
   go test ./tests

The tests verify that latency generation is deterministic and that the concurrent ping function returns one result per input host.
