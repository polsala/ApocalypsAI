# nightly-echo-chronicle

A whimsical concurrent HTTP latency checker. Given a list of URLs, it sends parallel GET requests and reports the minimum, average, and maximum response times. Perfect for scouting safe routes in the wasteland of the internet.

## Usage

```sh
go run ./src/main.go https://example.com https://golang.org
```

Output:

```
🔔 Echo Chronicle Report
✅ https://example.com – 123ms
✅ https://golang.org – 87ms
📊 Summary: min=87ms, avg=105ms, max=123ms
```

## Build

```sh
go build -o echo-chronicle ./src/main.go
```

## Test

```sh
go test ./tests
```
