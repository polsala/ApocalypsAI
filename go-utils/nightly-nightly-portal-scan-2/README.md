# nightly-portal-scan

A concurrent Go utility that scans a range of TCP ports on a host and reports open ports with a whimsical post‑apocalyptic flair.

## Installation

```sh
go build -o nightly-portal-scan ./src
```

## Usage

```sh
./nightly-portal-scan -host=example.com -start=1 -end=1024 -timeout=500ms
```

Outputs lines like:

⚡️ Port 80 is open! (Gateway to the wasteland)

## Flags

- `-host` (string, required): target hostname or IP.
- `-start` (int, default 1): starting port.
- `-end` (int, default 1024): ending port.
- `-timeout` (duration, default 500ms): connection timeout per port.
- `-workers` (int, default 100): number of concurrent workers.

## License

MIT
