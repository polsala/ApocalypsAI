# Apocalypse Ping Pong

A whimsical concurrent ping utility that checks latency to multiple hosts and reports them with fun animal metaphors.

## Usage

```sh
# Ping a list of hosts directly
go run ./src/main.go host1.com host2.com

# Or read hosts from a file (one per line)
go run ./src/main.go -f hosts.txt
```

## Output

Each line shows the host, latency in milliseconds, and a whimsical rating:

- `< 50ms`: "🐇 Rabbit speed"
- `50‑150ms`: "🐢 Turtle pace"
- `> 150ms`: "🦥 Sloth crawl"
- `error`: "❌ Unreachable"

## Build

```sh
go build -o apoc-ping ./src/main.go
```

## License

MIT
