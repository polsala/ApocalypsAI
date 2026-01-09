# nightly-echo-echo

A whimsical concurrent HTTP health checker that pings a list of URLs and reports their status with emojis.

## Features

- Concurrent requests with configurable concurrency limit.
- Timeout per request.
- Emoji-based status: ✅ for 2xx, ❌ for non-2xx, ⏳ for timeout.
- Simple command-line interface.

## Usage

```bash
# Check three URLs concurrently with default settings
./nightly-echo-echo https://example.com https://httpbin.org/status/404 https://httpbin.org/delay/2

# Set timeout to 1 second and concurrency to 2
./nightly-echo-echo -t 1 -c 2 https://example.com https://httpbin.org/delay/5
```

## Output

```
✅ https://example.com (200) 12.3ms
❌ https://httpbin.org/status/404 (404) 0.5ms
⏳ https://httpbin.org/delay/2 (timeout after 1s)
```

## Installation

```bash
go build -o nightly-echo-echo ./src/main.go
```

## License

MIT
