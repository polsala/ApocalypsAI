# Nightly Wasteland Ping Scorer

A whimsical Go utility that concurrently pings a list of URLs and assigns each a survival‑style status based on response latency.

## Features

* **Concurrent** – fires all requests in parallel.
* **Whimsical statuses** – *Radiant* (<100 ms), *Stable* (100‑300 ms), *Fading* (>300 ms), *Lost* (error/timeout).
* **Zero external dependencies** – pure Go standard library.

## Installation

```bash
go build -o wasteland-ping ./src/main.go
```

## Usage

```bash
./wasteland-ping -urls=https://example.com,https://api.github.com
```

You can also adjust the per‑request timeout:

```bash
./wasteland-ping -urls=https://example.com -timeout=3s
```

## Output

```
URL                            Latency    Status
-------------------------------------------------------
https://example.com            85ms       Radiant
https://api.github.com         210ms      Stable
https://slow.site              620ms      Fading
https://down.site              —          Lost
```

## Testing

Run the bundled tests with:

```bash
go test ./tests
```

All tests are deterministic and use local `httptest` servers; no external network calls are made.

## License

MIT © ApocalypsAI
