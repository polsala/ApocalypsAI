# nightly-portal-ping-multiplexer

**What it does**

A tiny Go utility that opens a *portal* to the afterlife of your network by concurrently attempting TCP connections to port 80 of a list of hosts. It reports success/failure and the round‑trip latency for each host.

**Why it’s useful**

- Quickly check reachability of many services without writing a script.
- Demonstrates Go’s lightweight concurrency (goroutines + channels).
- Fun, whimsical output (✅ for success, ❌ for failure).

**Installation**

```bash
# Clone the repository (or copy the utility folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-portal-ping-multiplexer
go build -o portal-ping-multiplexer ./src/main.go
```

**Usage**

```bash
./portal-ping-multiplexer example.com google.com nonexistent.local
```

Output example:

```
example.com: ✅ 85.123456ms
google.com: ✅ 42.987654ms
nonexistent.local: ❌ 3.001ms (dial tcp: lookup nonexistent.local: no such host)
```

**Testing**

Run the deterministic unit tests (they use a mock dialer, no real network calls):

```bash
go test ./tests
```

---

*Feel free to adapt the timeout or target port by editing the source.*
