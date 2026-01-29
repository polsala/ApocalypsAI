# nightly-portal-ping

A whimsical concurrent URL ping utility for the post‑apocalyptic wanderer. It checks the latency of multiple web portals in parallel and reports their status with themed messages.

## Usage

```sh
# Run without building (requires Go installed)
go run ./src/main.go https://example.com https://golang.org
```

Or build a binary:

```sh
go build -o portal-ping ./src/main.go
./portal-ping https://example.com https://golang.org
```

## Output

Each line shows the URL, latency in ms, and a themed status:

- **Radiant** – latency < 100 ms
- **Flickering** – latency 100‑300 ms
- **Dim** – latency > 300 ms

## Testing

```sh
go test ./...
```
