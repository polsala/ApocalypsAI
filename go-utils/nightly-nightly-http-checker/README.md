Nightly HTTP Checker
====================

A lightweight concurrent HTTP status checker that reports the health of a list of URLs.

Usage
-----

```bash
# Provide a file with one URL per line
go run ./src/main.go urls.txt

# Or pipe URLs via stdin
cat urls.txt | go run ./src/main.go
```

The utility prints each URL followed by its HTTP status code or an error message.

Options
-------

- `-c N` – number of concurrent workers (default 10).

Testing
-------

Run `go test ./...` to execute the test suite.
