# nightly-concurrent-ping

**What it does**

`nightly-concurrent-ping` is a tiny Go command‑line tool that takes a list of hostnames (or IP addresses) and measures how long it takes to establish a TCP connection to each host (default port 80).  All probes run concurrently, and the program prints a JSON object mapping each host to its measured latency in milliseconds (or an error string if the host is unreachable).

**Why it’s whimsical**

In a post‑apocalyptic world, you might need to know which abandoned radio towers still answer the call.  This tool pretends each tower is a web server and tells you how “loud” the echo is.

**Build & Run**

```bash
# Clone the repository (or copy the utility folder) and cd into it
cd utils/go-utils/nightly-concurrent-ping

# Build the binary (requires Go 1.22 or later)
go build -o nightly-concurrent-ping ./src/main.go

# Run against a few hosts
./nightly-concurrent-ping example.com google.com 8.8.8.8
```

**Output example**

```json
{
  "example.com": 42,
  "google.com": 15,
  "8.8.8.8": "dial timeout"
}
```

**Testing**

The utility ships with deterministic unit tests that mock the network layer, so they run offline without any real network access.

```bash
go test ./tests
```

**License**

MIT – see the repository root for details.
