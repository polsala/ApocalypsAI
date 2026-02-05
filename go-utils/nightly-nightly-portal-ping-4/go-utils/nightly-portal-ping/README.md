# nightly-portal-ping

**A whimsical, concurrent ping utility for the end‑times.**

## What it does
`portal-ping` pings a list of hosts (or IPs) in parallel, measures the round‑trip latency, and prints a colorful report that looks like a terminal‑screen from a post‑apocalyptic bunker.

## Install
```bash
# Clone the repository (or copy the utility folder) and build
cd go-utils/nightly-portal-ping
go build -o portal-ping ./src/main.go
```

## Usage
```bash
# Ping a comma‑separated list of hosts (default timeout 2s)
./portal-ping -hosts=example.com,8.8.8.8,192.0.2.1 -timeout=2s
```

### Flags
- `-hosts` (required): comma‑separated list of hostnames or IP addresses.
- `-timeout` (optional): per‑host timeout (e.g., `1s`, `500ms`). Default `2s`.
- `-concurrency` (optional): maximum number of simultaneous pings. Default `10`.

## Example output
```
⚡️ Scanning the wasteland…

[example.com]   23.4ms  ✅
[8.8.8.8]       12.1ms  ✅
[192.0.2.1]    timeout ❌

🛡️ All done. 2/3 hosts reachable.
```

## Testing
The utility ships with deterministic unit tests that mock network calls, so they run offline.
```bash
go test ./tests
```

## License
MIT © ApocalypsAI
