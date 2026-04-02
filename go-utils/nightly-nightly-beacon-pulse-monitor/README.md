# Nightly Beacon Pulse Monitor

A concurrent Go utility designed to check the 'pulse' (reachability and status) of various network beacons across the digital wasteland. It's crucial to know which signals are still strong and which have faded into the static.

## Usage

Run the utility with a list of URLs or IP addresses you wish to monitor. Each will be checked concurrently.

```bash
go run src/main.go <url1> <url2> ...
```

### Example:

```bash
go run src/main.go https://google.com http://localhost:8080 https://nonexistent-beacon.invalid
```

This will output the status of each beacon, indicating if its pulse is strong, faint, or lost.

## Building from Source

To build the executable:

```bash
go build -o beacon-pulse-monitor src/main.go
./beacon-pulse-monitor <url1> <url2>
```

## Tests

To run the tests, navigate to the utility's root directory and execute:

```bash
go test ./tests
```

Tests use `net/http/httptest` to simulate network responses, ensuring they are deterministic and do not rely on external network access.
