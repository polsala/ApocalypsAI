# nightly-concurrent-ping-pong

**What it does**

`nightly-concurrent-ping-pong` is a tiny Go command‑line tool that pings a list of hosts **concurrently** (using TCP connection attempts to port 80) and prints a playful report with emojis:

- ✅ host reachable – shows latency in milliseconds
- ❌ host unreachable – shows the error

The tool is useful for quick network sanity checks, especially when you need to verify many endpoints at once without waiting for each request to finish sequentially.

---

## Installation

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd go-utils/nightly-concurrent-ping-pong
go build -o pingpong src/main.go
```

The binary will be named `pingpong`.

---

## Usage

```bash
./pingpong example.com google.com nonexisting.invalid
```

Output example:

```
🔔 Ping Pong Report 🔔
✅ example.com: 38 ms
✅ google.com: 12 ms
❌ nonexisting.invalid: dial tcp: lookup nonexisting.invalid: no such host
```

---

## How it works

- The program reads hostnames from command‑line arguments.
- For each host it spawns a goroutine that attempts a TCP connection to port 80 with a 2‑second timeout.
- Results are sent over a channel back to the main goroutine, which prints a formatted report.
- The ping logic is abstracted behind a `pingFunc` variable, allowing the test suite to replace it with a deterministic mock.

---

## Testing

```bash
go test ./tests
```

The test suite replaces the real network call with a mock implementation, ensuring deterministic, offline tests.
