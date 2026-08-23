# Nightly Beacon Signal Verifier

## Summary

The `nightly-beacon-signal-verifier` is a whimsical-yet-useful Go utility designed to concurrently check the reachability and response time of critical network "beacons" (endpoints). In a world of temporal anomalies and void whispers, ensuring your signals are still alive is paramount. This tool helps you monitor the pulse of your network infrastructure or external services.

It takes a list of `host:port` pairs as arguments, pings them using TCP, and reports whether each beacon is "UP" or "DOWN" along with its measured latency.

## Usage

### Build

To build the utility, navigate to the `src` directory and run:

```bash
go build -o nightly-beacon-signal-verifier
```

### Run

Execute the compiled binary with a list of `host:port` beacons:

```bash
./nightly-beacon-signal-verifier <beacon1> [beacon2...] [--timeout=<duration>]
```

**Arguments:**

*   `<beacon>`: A network endpoint specified as `host:port` (e.g., `google.com:80`, `192.168.1.1:22`, `localhost:8080`).
*   `--timeout=<duration>`: (Optional) Specifies the maximum time to wait for a connection. Defaults to `3s` (3 seconds). Duration can be specified like `500ms`, `2s`, `1m`, etc.

**Examples:**

Check if Google's web server and a local SSH port are reachable:

```bash
./nightly-beacon-signal-verifier google.com:80 localhost:22
```

Check multiple services with a custom timeout:

```bash
./nightly-beacon-signal-verifier example.com:443 myapi.internal:8080 --timeout=5s
```

### Output

The utility will print a report for each beacon, indicating its status (UP/DOWN) and latency if successful, or an error message if it failed. The program will exit with a non-zero status code (`1`) if any beacon is reported as DOWN or if there's an error parsing an argument, making it suitable for CI/CD pipelines or monitoring scripts.

```
--- Beacon Signal Verification Report ---
✅ google.com:80 - UP (Latency: 12.34ms)
❌ example.com:443 - DOWN (Error: connection refused)
✅ myapi.internal:8080 - UP (Latency: 5.67ms)
❌ invalid-beacon - DOWN (Error: Invalid beacon 'invalid-beacon': invalid format. Expected host:port)
-----------------------------------------
```

## Development

### Project Structure

```
.gitignore
README.md
src/
  main.go
tests/
  main_test.go
```

### Dependencies

This utility uses only standard Go library packages (`fmt`, `net`, `os`, `strconv`, `strings`, `sync`, `time`). No external modules are required.

### Testing

To run the tests, navigate to the `tests` directory and execute:

```bash
go test -v
```

The tests use a `MockPinger` to simulate network responses, ensuring they are deterministic and do not rely on actual network connectivity.
