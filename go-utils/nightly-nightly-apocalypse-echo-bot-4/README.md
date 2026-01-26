# Apocalyptic Echo Bot

A whimsical concurrent Go TCP server that echoes back any line sent by a client, prefixed with a random apocalypse‑themed phrase (e.g., "Doomsday", "The Last Sunrise").

## Build

```sh
go build -o echo-bot ./src
```

## Run

```sh
# default listens on localhost:4000
./echo-bot

# custom address
ADDRESS=0.0.0.0:12345 ./echo-bot
```

## Example

```sh
$ nc localhost 4000
hello world
Doomsday: hello world
```

## Test

```sh
go test ./tests
```
