# nightly-portal-ping-mux

**A whimsical concurrent TCP ping multiplexer**

## Overview
`nightly-portal-ping-mux` is a tiny Go utility that opens a *portal* to a list of hosts, measures how quickly the portal opens (i.e., how fast a TCP connection can be established), and then prints a summary of the latency statistics:

- **min** latency
- **average** latency
- **max** latency

The tool runs all pings concurrently, making it perfect for quick health‑checks of many services.

## Build
```bash
# Clone the repository (or copy the generated folder) and build
cd nightly-portal-ping-mux
go build -o portal-ping ./src/main.go
```

## Usage
```bash
# Pass a space‑separated list of host:port pairs
./portal-ping example.com:80 8.8.8.8:53 localhost:22
```

The output will look like:
```
Portal opened to example.com:80 – latency: 12.3ms
Portal opened to 8.8.8.8:53 – latency: 8.7ms
Portal opened to localhost:22 – latency: 0.4ms

Latency stats – min: 0.4ms | avg: 7.1ms | max: 12.3ms
```

## Testing
```bash
go test ./tests
```

The test suite uses a mock dialer, so no real network traffic is generated.

## License
MIT © ApocalypsAI
