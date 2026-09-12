# Nightly Radiation Ping

**Nightly Radiation Ping** is a playful, concurrent command‑line tool written in Go. It pings a list of URLs and translates the measured latency into a whimsical "radiation level" – Low, Medium, or High – giving you a post‑apocalyptic feel for the health of your services.

## Features

- **Concurrent**: Pings multiple URLs in parallel (default max 5 workers).
- **Radiation Mapping**:
  - `< 100ms` → **Low** radiation
  - `100‑300ms` → **Medium** radiation
  - `> 300ms` → **High** radiation
- **Zero external dependencies** – pure Go standard library.
- **Deterministic offline tests** using `httptest` servers.

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-radiation-ping

# Build the binary
go build -o radiation-ping ./src/main.go
```

## Usage

```bash
# Ping a handful of URLs
./radiation-ping https://example.com https://golang.org https://nonexistent.invalid
```

Output example:

```
https://example.com  84ms   Low
https://golang.org   152ms  Medium
https://nonexistent.invalid  error: Get "https://nonexistent.invalid": dial tcp: lookup nonexistent.invalid: no such host
```

You can also pipe a list of URLs (one per line) via `xargs`:

```bash
cat urls.txt | xargs ./radiation-ping
```

## Testing

Run the unit tests with:

```bash
go test ./tests
```

The tests use mocked HTTP servers, so they are deterministic and require no network access.

## License

MIT © ApocalypsAI
