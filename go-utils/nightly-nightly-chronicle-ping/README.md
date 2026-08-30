Nightly Chronicle Ping
=======================

A tiny Go utility that pings a list of hosts concurrently and prints a short report of the latency for each reachable host.  It is deliberately lightweight and works offline in tests by allowing the ping function to be mocked.

Features
--------
* Accepts hosts as command‑line arguments or via STDIN (one per line).
* Performs the checks in parallel using Go goroutines.
* Shows latency in milliseconds or an error message if the host is unreachable.
* Simple JSON‑compatible output for piping into other tools.

Installation
------------
```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-chronicle-ping/src
go build -o chronicle-ping main.go
```

Usage
-----
```bash
# Ping a few hosts supplied as arguments
./chronicle-ping example.com google.com github.com

# Or pipe a list of hosts from a file
cat hosts.txt | ./chronicle-ping
```

The output looks like:
```
example.com: 84ms
google.com: 27ms
github.com: error: dial timeout
```

Testing
-------
The test suite lives in `tests/main_test.go` and runs with the standard Go test runner:
```bash
go test ./...
```
The tests replace the network‑calling function with a deterministic mock, so they run without any external network access.

License
-------
MIT – see the LICENSE file in the repository root.
