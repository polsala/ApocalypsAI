# Nightly Chrononaut Ping Swarm

**Overview**
A whimsical yet practical Go utility that pings multiple hosts concurrently, simulating a fleet of space‑faring chrononauts checking the health of distant planets. It reports latency statistics and highlights any unreachable hosts.

**Features**
- Fully concurrent using goroutines and a worker pool.
- Configurable timeout (default 2 seconds).
- Sorted output by fastest response.
- Zero external dependencies – uses only the Go standard library.

**Installation**
```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-chrononaut-ping-swarm
# Build the binary
go build -o ping-swarm ./src/main.go
```

**Usage**
```bash
# Ping a list of hosts (space‑separated)
./ping-swarm example.com google.com nonexistent.invalid
```

**Example Output**
```
Host                 Latency   Status
------------------------------------------
example.com          42ms      OK
google.com           58ms      OK
nonexistent.invalid  -        ERROR: dial tcp: lookup nonexistent.invalid: no such host
```

**Testing**
Run the deterministic unit tests (network calls are mocked):
```bash
go test ./... 
```

**License**
MIT © ApocalypsAI
