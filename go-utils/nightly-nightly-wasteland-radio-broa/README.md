# Nightly Wasteland Radio Broadcast

A whimsical Go utility that simulates a post‑apocalyptic radio station. It schedules a series of broadcast messages and serves a JSON schedule over HTTP.

## Build

```sh
go build -o radio .
```

## Run

```sh
./radio -port 8080
```

The server will start and begin broadcasting messages every minute. Access the schedule:

```sh
curl http://localhost:8080/schedule
```

## How it works

- A list of pre‑written broadcast messages is defined.
- Each message is assigned a broadcast time starting from the server start time, spaced one minute apart.
- A background goroutine updates the schedule (currently generated once at start).
- `/schedule` returns the upcoming messages with their timestamps.

## Testing

```sh
go test ./...
```
