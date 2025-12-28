Nightly Concurrent HTTP Checker

A lightweight Go utility that concurrently checks the health of multiple HTTP endpoints and reports their status codes.

Usage:
  go run main.go https://example.com https://google.com

Options:
  -concurrency int
        Number of concurrent workers (default 5)

Output:
  URL: https://example.com - Status: 200
  URL: https://google.com - Status: 200
