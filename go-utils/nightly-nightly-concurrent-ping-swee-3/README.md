# nightly-concurrent-ping-sweeper

**What it does**

A tiny Go program that pings (via a TCP connection) a list of hosts concurrently and prints a JSON array with the result for each host.  It’s useful for quickly checking service availability across many endpoints without leaving your terminal.

**Features**

- Accepts hosts as command‑line arguments or via STDIN (one per line).
- Configurable per‑host timeout (`-t` flag, default 1000 ms).
- Fully concurrent using goroutines and a `sync.WaitGroup`.
- Outputs nicely indented JSON for easy piping into `jq` or other tools.

**Installation**

```bash
# Clone the repository (or copy the src/main.go file)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-concurrent-ping-sweeper

# Build the binary (requires Go 1.20+)
go build -o ping-sweeper src/main.go
```

**Usage**

```bash
# Pass hosts as arguments
./ping-sweeper -t 1500 example.com:80 google.com:443

# Or pipe a list of hosts (host:port) via STDIN
cat hosts.txt | ./ping-sweeper -t 500
```

**Example output**

```json
[
  {
    "host": "example.com:80",
    "success": true,
    "latency_ms": 23.4
  },
  {
    "host": "nonexistent:1234",
    "success": false,
    "error": "dial tcp 93.184.216.34:1234: connect: connection refused"
  }
]
```

**Testing**

Run the bundled tests with:

```bash
go test ./...
```

The tests spin up local TCP listeners to verify both successful connections and timeout handling.
