# Nightly Concurrent Ping

A whimsical Go utility that pings multiple hosts concurrently and reports each latency.

## What it does
- Spawns a goroutine for every host you provide
- Uses the system `ping` command (single packet, short timeout)
- Prints the latency (e.g., `12.3ms`) or `error` if the host is unreachable

## Why itâs useful
When you need a quick sanityâcheck of several endpoints, running `ping` sequentially can be slow. This tool demonstrates Go's lightweight concurrency while giving you a handy networkâstatus snapshot.

## Installation
```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-concurrent-ping

# Build the binary
go build -o concurrent-ping ./src/main.go
```

## Usage
```bash
./concurrent-ping example.com google.com 8.8.8.8
```

Output example:
````
Ping results:
example.com: 23ms
google.com: 15ms
8.8.8.8: error
````

## Testing
```bash
go test ./tests
```

The test suite uses a mock ping executor so it runs offline and deterministically.

