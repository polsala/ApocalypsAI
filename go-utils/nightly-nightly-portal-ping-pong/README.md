# Nightly Portal Ping Pong

A whimsical yet useful Go utility that concurrently measures network latency to a list of hosts and ranks them from fastest to slowest. Perfect for quickly checking the health of your services or just having fun seeing which endpoint wins the "ping pong" tournament.

## Features

- Concurrent latency checks using goroutines.
- Configurable timeout per host.
- Human‑readable ranking with playful messages.
- Zero external dependencies (standard library only).

## Installation

```sh
go build -o portal-ping-pong ./src/main.go
```

## Usage

```sh
./portal-ping-pong example.com:80 google.com:443 192.0.2.1:22
```

Output:

```
🏆 1️⃣ example.com:80 – 12.3ms
🥈 2️⃣ google.com:443 – 45.6ms
🥉 3️⃣ 192.0.2.1:22 – timeout
```

## Testing

```sh
go test ./tests
```

The tests use a mock latency function, so they run offline and deterministically.

## License

MIT
