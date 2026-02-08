# Nightly Traffic Portal Simulator

A whimsical concurrent Go utility that simulates traffic to a list of URLs, useful for quick load‑testing or checking endpoint health. It launches a configurable number of goroutines that repeatedly send GET requests for a given duration and reports statistics.

## Build

```sh
go build -o traffic-portal ./src
```

## Usage

```sh
./traffic-portal -urls url1,url2,... -concurrency 10 -duration 30s
```

Or provide a file with URLs (one per line):

```sh
./traffic-portal -file urls.txt -concurrency 5 -duration 1m
```

## Flags

- `-urls` : comma‑separated list of target URLs.
- `-file` : path to a file containing one URL per line.
- `-concurrency` : number of parallel workers (default **5**).
- `-duration` : how long to run the simulation (e.g., `10s`, `2m`) (default **10s**).

## Output

```
Total requests: 1234
Successful: 1220
Failed: 14
Average latency: 45.6ms
```

## Testing

```sh
go test ./...
```
