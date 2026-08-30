# Ghost Ping

A whimsical concurrent ping utility that checks the reachability of hosts and reports latency with ghostly emojis.

## Installation

```bash
go build -o ghost-ping ./src
```

## Usage

```bash
# Ping hosts passed as arguments
./ghost-ping example.com 8.8.8.8

# Or read hosts from a file (one per line)
./ghost-ping -f hosts.txt
```

## Output

The tool prints a table with the host, measured latency, and an emoji indicating the result:

- `👻` – lightning‑fast (< 100 ms)
- `🕸️` – moderate (100 ms – 300 ms)
- `🧟` – slow (> 300 ms)
- `⚰️` – unreachable / error

## Example

```text
Host               Latency   Status
example.com        42ms      👻
nonexistent.tld    —         ⚰️
```

## License

MIT © ApocalypsAI
