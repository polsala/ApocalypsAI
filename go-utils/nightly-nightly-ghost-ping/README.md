# nightly-ghost-ping

**nightly-ghost-ping** is a tiny Go command‑line tool that concurrently checks the reachability of one or more hosts by attempting a TCP connection to port 80.  It reports the latency (or timeout) for each host, prefixed with a friendly ghost emoji (👻).

## Features

- **Concurrent**: each host is probed in its own goroutine, making the overall scan fast.
- **Deterministic output**: results are printed in the order they finish, each line is self‑contained.
- **Whimsical**: ghost emojis turn a boring network check into a fun experience.
- **Testable**: the core ping logic is isolated in a separate package and fully mocked in the test suite.

## Installation

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-ghost-ping
go build -o ghost-ping ./src/main.go
```

## Usage

```bash
./ghost-ping example.com google.com nonexistent.local
```

Sample output:

```
👻 example.com: 23 ms
👻 google.com: 45 ms
👻 nonexistent.local: timeout or error (dial tcp: lookup nonexistent.local: no such host)
```

## Testing

The test suite uses a mock `dialContext` to simulate network latency and timeouts, ensuring deterministic, offline tests.

```bash
go test ./tests
```

## License

MIT © ApocalypsAI community
