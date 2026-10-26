# Quick Wit Ping

A concurrent ping utility that checks latency to multiple hosts and rates them with whimsical animal metaphors (e.g., cheetah, rabbit, turtle). Useful for quick network health checks with a smile.

## Installation

```sh
go build -o quick-wit-ping ./src/main.go
```

## Usage

```sh
./quick-wit-ping host1.com host2.com 8.8.8.8
```

If no arguments are provided, the utility reads hosts line‑by‑line from **stdin**.

## Output

```
host1.com: 23ms – 🐆 Cheetah (fast)
host2.com: 112ms – 🐇 Rabbit (moderate)
8.8.8.8: 210ms – 🐢 Turtle (slow)
```

## How it works

- Uses goroutines to ping up to 10 hosts concurrently.
- Measures latency with a TCP dial to port 80 (fallback to 443 if needed).
- Maps latency to animal emojis for a whimsical rating.

## License

MIT License
