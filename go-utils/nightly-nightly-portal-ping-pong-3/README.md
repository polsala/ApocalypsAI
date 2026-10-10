# nightly-portal-ping-pong

A whimsical concurrent port scanner that darts across a range of ports and reports which ones are open. Perfect for quick network checks in a post‑apocalyptic bunker.

## Usage

```sh
go run src/main.go -host localhost -ports 8000,8001,8080
```

The program prints a list of open ports, e.g.:

```
Open ports on localhost: 8000 8080
```

## How it works

- Parses a comma‑separated list of ports.
- Launches a goroutine per port (limited by a semaphore to avoid overwhelming the system).
- Uses a short TCP dial timeout (default 500 ms) to test each port.
- Collects results via channels and prints the open ports.

## Testing

Run `go test ./...` to execute the deterministic unit tests which spin up local listeners.
