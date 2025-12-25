# nightly-concurrent-ping-pong

**What it does**

`nightly-concurrent-ping-pong` is a tiny Go command‑line tool that pings a list of hosts *concurrently* and prints a fun, radio‑style report of the round‑trip times.  It’s useful for quick network sanity checks and adds a dash of apocalypse‑themed flair to the output.

**Features**

- Concurrent probing of any number of hosts (default timeout 2 seconds).
- Uses TCP connect‑time as a proxy for latency (no raw ICMP needed, works without root).
- Optional `-quiet` flag to suppress the radio‑chatter and emit CSV for scripting.
- Fully unit‑tested with a mock dialer – tests run offline.

**Installation**

```bash
# Clone the repository (or copy the utility folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/go-utils/nightly-concurrent-ping-pong

# Build the binary
go build -o pingpong ./src/main.go
```

**Usage**

```bash
# Basic usage – provide hostnames or IPs as arguments
./pingpong example.com 8.8.8.8

# Quiet CSV output for pipelines
./pingpong -quiet example.com 8.8.8.8
```

**Sample output**

```
[Radio] :: Initiating transmission to the wasteland...
[Radio] :: example.com responded in 42ms – signal clear.
[Radio] :: 8.8.8.8 responded in 18ms – static crackles.
[Radio] :: All stations checked. End of broadcast.
```

**Testing**

```bash
go test ./tests
```

The test suite uses a mock dialer, so no network access is required.
