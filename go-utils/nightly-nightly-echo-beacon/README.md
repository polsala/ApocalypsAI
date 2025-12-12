# nightly-echo-beacon

A whimsical yet practical utility that lets machines on the same local network discover each other by broadcasting and listening for short UDP echo beacons.

## Features

- Concurrent broadcasting of a custom message every second.
- Listening mode that prints received messages in real time.
- Pure Go implementation, no external dependencies.
- Mock‑friendly design for deterministic offline tests.

## Build & Run

```sh
go build -o echo-beacon ./src/main.go
# Broadcast mode
./echo-beacon -mode=broadcast -msg="hello from the wasteland" -port=9999
# Listen mode
./echo-beacon -mode=listen -port=9999
```

## Testing

```sh
go test ./tests
```

The tests use a mock network layer, so they run without any real network access.

## License

MIT
