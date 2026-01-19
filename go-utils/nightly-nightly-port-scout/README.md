# nightly-port-scout

A whimsical concurrent TCP port scanner for the post‑apocalyptic wasteland. Quickly discover open ports on a target host using Go's goroutine magic.

## Usage

```sh
go run ./src/main.go -host example.com -start 1 -end 1024 -timeout 500ms -workers 100
```

**Options**

- `-host`   target hostname or IP (required)
- `-start`  starting port (default 1)
- `-end`    ending port (default 1024)
- `-timeout` connection timeout (e.g., 500ms)
- `-workers` maximum concurrent scans (default 100)

The program prints open ports, one per line.

## How it works

Spawns a pool of workers that attempt to `net.DialTimeout` each port. Open ports are collected and displayed.

## Tests

Run `go test ./...` to execute deterministic tests that spin up temporary listeners.
