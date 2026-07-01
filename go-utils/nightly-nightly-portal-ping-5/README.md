# nightly-portal-ping

A whimsical concurrent port scanner that pings a range of ports and reports open ones with playful messages.

## Build

```sh
go build -o portal-ping ./src
```

## Usage

```sh
./portal-ping -host example.com -start 80 -end 85 -workers 10
```

The tool will scan ports 80‑85 on `example.com` using up to 10 concurrent workers and print messages like:

```
✨ Port 80 is open! 🎉
❌ Port 81 is closed.
```

## How it works

- Uses a worker pool to scan ports concurrently.
- Each port is probed with a short timeout.
- Results are printed with emojis for a whimsical touch.

## Testing

```sh
go test ./...
```
