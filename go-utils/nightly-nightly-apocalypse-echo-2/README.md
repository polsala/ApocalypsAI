# nightly-apocalypse-echo

A whimsical Go utility that runs a TCP echo server. Every line received is echoed back prefixed with an apocalyptic warning "[Doom] ". Useful for testing network clients and adding a bit of fun to your dev environment.

## Usage

```sh
go run ./src/main.go
```

The server listens on a random available port and prints the address, e.g.:

```
Listening on 127.0.0.1:54321
```

Connect with netcat:

```sh
nc 127.0.0.1 54321
hello
# receives:
[Doom] hello
```

## Library

The package also provides `RunServer()` which returns the listening address and a shutdown function, useful for programmatic use and testing.

## Tests

Run `go test ./...` to execute the deterministic unit tests.
