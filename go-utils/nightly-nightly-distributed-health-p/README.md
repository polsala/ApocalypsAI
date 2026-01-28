# Nightly Distributed Health Probe

## Summary

The `nightly-distributed-health-probe` is a Go-based utility designed to concurrently probe a list of URLs or endpoints. It reports on their availability, the 'temporal echo' (response time), and 'aura code' (HTTP status code), helping you monitor the vitality of your digital outposts.

## Usage

### Build

To build the utility, navigate to the `src` directory and run:

```bash
go build -o health-probe main.go
```

### Run

You can specify URLs directly via the `-urls` flag (comma-separated) or provide a file containing one URL per line using the `-file` flag.

```bash
./health-probe -urls "https://www.google.com,https://www.github.com" -concurrency 5 -timeout 5s
```

```bash
# Assuming urls.txt contains:
# https://www.example.com
# https://nonexistent.invalid
./health-probe -file urls.txt -concurrency 10 -timeout 3s
```

### Flags

*   `-urls string`: Comma-separated list of URLs to probe. (e.g., `"http://localhost:8080,https://api.example.com"`)
*   `-file string`: Path to a file containing URLs, one per line.
*   `-concurrency int`: Maximum number of concurrent probes. (Default: `5`)
*   `-timeout duration`: Timeout for each HTTP request. (Default: `5s`)

## Output

The utility will print a report for each probed URL, indicating its status, temporal echo, and aura code. If an error occurs, it will be noted as a 'VOID ANOMALY'.

```
Probing https://www.google.com...
  Status: OK
  Temporal Echo: 123.45ms
  Aura Code: 200

Probing https://nonexistent.invalid...
  Status: VOID ANOMALY
  Temporal Echo: N/A
  Aura Code: N/A (Error: dial tcp: lookup nonexistent.invalid: no such host)
```

## Development

### Tests

To run the tests, navigate to the `tests` directory and run:

```bash
go test -v
```
