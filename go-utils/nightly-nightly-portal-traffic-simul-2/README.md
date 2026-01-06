# nightly-portal-traffic-simulator

Simulates traffic through a mystical portal. The service spawns a configurable number of traveler goroutines that periodically "enter" the portal. It tracks total travelers, current active travelers, and provides a JSON metrics endpoint.

## Usage

```sh
go run src/main.go -port 8080 -workers 5 -duration 10s
```

- `-port` : HTTP port for metrics (default 8080)
- `-workers` : number of concurrent traveler generators (default 3)
- `-duration` : how long each traveler stays before exiting (e.g., 5s)

Visit `http://localhost:8080/metrics` to see live stats:

```json
{
  "total_travelers": 42,
  "active_travelers": 3
}
```

## Build

```sh
go build -o portal-sim src/main.go
```

## Test

```sh
go test ./...
```
