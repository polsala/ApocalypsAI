# nightly-portal-ping-pong

A whimsical concurrent ping utility that checks reachability of multiple hosts and reports results with emojis.

## Usage

```sh
go run ./src/main.go host1.com host2.com
```

Outputs each host with ✅ or ❌ and a summary.

## Build

```sh
go build -o pingpong ./src/main.go
```

## Test

```sh
go test ./tests
```
