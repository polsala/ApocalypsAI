# nightly-concurrent-ping

Concurrently ping multiple HTTP endpoints and display latency with whimsical emojis.

## Usage

```sh
go run ./src/main.go https://example.com https://golang.org
```

The program will output something like:

```
🛰️ example.com responded in 42ms
🚀 golang.org responded in 15ms
```

- Fast responses get a 🚀 emoji, moderate responses get a 🛰️, and slow responses get a 🐢.
- If a request fails, a 💥 emoji is shown with the error.

## How it works

- Each URL is processed in its own goroutine.
- The round‑trip time is measured with `time.Now()`.
- Results are collected via a channel, sorted by latency, and printed with an emoji that reflects speed.
- The implementation uses only the Go standard library, so no external dependencies are required.

## Testing

Run the test suite with:

```sh
go test ./...
```

The tests use `httptest` servers with deterministic delays, ensuring offline, repeatable results.
