# Nightly Portal Ping Multiplexer

**Utility name:** `nightly-portal-ping-multiplexer`

## Overview

`portal-ping-multiplexer` is a tiny Go command‑line tool that concurrently sends HTTP GET requests to a list of URLs (your “portals”) and reports the round‑trip latency for each.  It’s useful for:

- Quickly checking the health of multiple services.
- Spotting latency spikes before they become a full‑blown temporal rift.
- Adding a dash of whimsical flair to your monitoring scripts.

The tool is completely self‑contained, has no external dependencies beyond the Go standard library, and includes deterministic unit tests that use mock HTTP servers.

## Installation

```bash
# Clone the repository (or copy the utility folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd go-utils/nightly-portal-ping-multiplexer

# Build the binary
go build -o portal-ping-multiplexer ./src/main.go
```

## Usage

```bash
./portal-ping-multiplexer [options] <url1> <url2> ...
```

### Options

- `-timeout <seconds>` – Maximum time to wait for each request (default: 2 seconds).

### Example

```bash
./portal-ping-multiplexer -timeout 3 https://example.com https://api.example.org
```

Output:

```
🌀 Portal Ping Results 🌀
https://example.com -> 42 ms
https://api.example.org -> 118 ms
```

If a request fails or times out, the tool prints a ✖ symbol:

```
https://dead.portal -> ✖ timeout/error
```

## Testing

The utility ships with a Go test suite that runs entirely offline using `net/http/httptest` servers.

```bash
go test ./tests
```

All tests should pass.

## License

MIT © ApocalypsAI community
