# nightly-go-apocalypse-echo

## Summary

A whimsical concurrent TCP echo server written in Go. Each line received from a client is echoed back prefixed with a random apocalypse‑themed phrase (e.g., "The skies darken:", "Radiation levels rise:").

## Usage

```sh
go run ./src/main.go [port]
```

If no port is provided, the server defaults to `8080`.

Connect with `nc` (netcat) or any TCP client:

```sh
nc localhost 8080
Hello world
The skies darken: Hello world
```

## Building

```sh
go build -o apocalypse-echo ./src/main.go
```

## Testing

```sh
go test ./tests
```
