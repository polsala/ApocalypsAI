# Nightly Echo Scout

## Overview

Nightly Echo Scout is a whimsical concurrent URL pinger that scans a list of web endpoints and reports their latency with radio‑style messages. Perfect for post‑apocalyptic signal hunting or quick health checks.

## Installation

```sh
go build -o nightly-echo-scout ./src
```

## Usage

```sh
./nightly-echo-scout https://example.com https://golang.org
```

## Sample Output

```
🔊 https://example.com - Signal received in 42ms 🎶
❌ https://badhost - Error: Get "https://badhost": dial tcp: lookup badhost: no such host
```

The utility runs each request in its own goroutine, making full use of Go's concurrency model.

## Testing

Run the test suite with:

```sh
go test ./tests
```
