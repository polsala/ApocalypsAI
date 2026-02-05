# nightly-concurrent-ping

A whimsical concurrent ping utility for the apocalypse. It pings multiple URLs in parallel, measures latency, and outputs a survival score.

## Usage

```sh
go run ./src/main.go -urls=https://example.com,https://example.org -timeout=2
```

- `-urls` : comma‑separated list of URLs to ping.
- `-timeout` : per‑request timeout in seconds (default 5).

## Output

The program prints a JSON object with the following fields:

- `total` – total number of URLs processed.
- `success` – how many responded with a 2xx status.
- `failed` – how many failed or timed‑out.
- `min_ms`, `max_ms`, `avg_ms` – latency statistics (in milliseconds) for successful requests.
- `survival_score` – a 0‑100 score derived from success rate and latency (higher is better).
- `details` – an array with per‑URL results.

## Build

```sh
go build -o concurrent-ping ./src/main.go
```

## Tests

```sh
go test ./tests
```

The tests use local HTTP test servers, so they run offline and deterministically.
