# Nightly Echo-Location Pinger

## Summary

The `nightly-echo-location-pinger` is a whimsical-yet-useful Go utility designed to concurrently measure the HTTP response latency to multiple network endpoints. Think of it as sending out sonic pings into the digital void and timing how long it takes for the echoes to return. It reports the latency for each 'echo chamber' (URL).

## Usage

To run the pinger, simply provide a list of URLs as command-line arguments:

```bash
go run src/main.go https://www.google.com https://www.github.com http://localhost:8080
```

Alternatively, you can build and run the executable:

```bash
go build -o echo-pinger src/main.go
./echo-pinger https://www.google.com https://www.github.com
```

### Output Example

```
--- Initiating Echo-Location Pings ---
Pinging https://www.google.com...
Pinging https://www.github.com...

--- Echo-Location Report ---
https://www.google.com: 50ms
https://www.github.com: 75ms
----------------------------
```

## Development

### Prerequisites

- Go (version 1.16 or higher)

### Building

```bash
go build -o echo-pinger src/main.go
```

### Running Tests

```bash
go test ./tests
```
