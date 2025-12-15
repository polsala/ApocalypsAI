# Apocalyptic Echo Bot

A whimsical concurrent Go echo server that prefixes each incoming line with a random apocalyptic phrase. Useful for testing network clients and adding drama to your logs.

## Build

```sh
go build -o echo-bot ./src
```

## Run

```sh
./echo-bot [port]
```

If no port is provided, defaults to **8080**.

## Example

```sh
$ nc localhost 8080
Hello world
The ground trembles: Hello world
```

## Test

```sh
go test ./...
```
