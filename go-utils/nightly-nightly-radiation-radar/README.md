# Radiation Radar

A whimsical Go utility that concurrently checks the latency of a list of URLs (or hostnames) and displays a colorful radar of "radiation levels" indicating how fast each endpoint responds. Useful for quick health checks of services, with a fun post‑apocalyptic theme.

## Usage

```sh
go run ./src/main.go https://example.com https://golang.org
```

Output (example):

```
⚡️ https://golang.org  23ms  [██████      ] Low radiation
☢️ https://example.com  187ms [███         ] Moderate radiation
☣️ http://slow.test    842ms [█           ] High radiation
```

## How it works

- Accepts URLs as command‑line arguments.
- Launches a goroutine per URL, measures time to complete an HTTP GET.
- Results are collected, sorted by latency, and displayed with emoji‑based radiation levels.

## Testing

Run `go test ./...` to execute the deterministic unit tests that mock HTTP servers with predefined delays.
