# Portal Ping

A whimsical concurrent port scanner that discovers open ports on a target host and celebrates each find with a quirky message.

## Usage

```sh
go run ./src/main.go -host localhost -ports 8000-8010 -workers 100
```

## Flags

- `-host`   target hostname or IP (default `"localhost"`)
- `-ports`  port range in the form `start-end` (default `"1-1024"`)
- `-workers` number of concurrent workers (default `100`)

## Build

```sh
go build -o portal-ping ./src/main.go
```

## Example Output

```
🔍 Scanning localhost ports 8000-8010 with 100 workers...
✨ Port 8000 is open! The portal welcomes you.
❌ Port 8001 is closed.
... (more lines)
```

The tool is safe, deterministic, and works offline – perfect for nightly fun in the wasteland.
