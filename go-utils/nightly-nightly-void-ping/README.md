# nightly-void-ping

A whimsical concurrent HTTP health checker that reports the status of your URLs with post‑apocalyptic flair.

## Features
- Checks multiple URLs in parallel using Go goroutines.
- Colorful output: ✅ for alive, ☢️ for dead.
- Optional input file (`-file`) with one URL per line.
- Built‑in timeout (5s) to avoid hanging on dead endpoints.

## Installation
```sh
go build -o nightly-void-ping ./src
```

## Usage
```sh
# Check URLs passed as arguments
./nightly-void-ping https://example.com https://nonexistent.tld

# Check URLs from a file
./nightly-void-ping -file urls.txt
```

## Example Output
```
✅ https://example.com responded with 200 OK
☢️ https://nonexistent.tld timed out after 5s
```

## Testing
```sh
go test ./...
```
