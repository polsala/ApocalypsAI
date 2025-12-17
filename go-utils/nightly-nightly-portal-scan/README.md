# nightly-portal-scan

A whimsical concurrent TCP port scanner for the post‑apocalypse. It scans a range of ports on a host using configurable concurrency and prints any open ports with a fun message.

## Build

```sh
go build -o nightly-portal-scan ./src
```

## Usage

```sh
./nightly-portal-scan -host localhost -start 8000 -end 8010 -c 100
```

Will output lines like:

```
🔎 Port 8000 is open! The portal hums...
```

## Testing

```sh
go test ./tests
```
