# Nightly Chronal Drift Detector

## Overview
In the chaotic temporal landscape of the post-apocalypse, maintaining synchronized chronometers is paramount. The `nightly-chronal-drift-detect` utility acts as your personal temporal integrity monitor, scanning designated 'time-beacons' (remote servers) to detect any 'chronal drift' – significant time discrepancies between your local chronometer and theirs.

This tool is crucial for distributed systems, ensuring that all your operational nodes are marching to the same temporal beat, preventing data corruption, inconsistent logs, and general temporal chaos.

## How it Works
The utility performs a series of concurrent HTTP HEAD requests to specified URLs. It extracts the `Date` header from the server's response, which represents the server's current time. This remote time is then compared against your local system's UTC time. Any significant difference is reported as 'chronal drift'.

## Features
*   **Concurrent Scanning**: Utilizes Go's goroutines to check multiple time-beacons simultaneously for efficiency.
*   **Drift Detection**: Clearly reports the time difference (drift) for each beacon.
*   **Error Handling**: Gracefully handles unreachable beacons or invalid responses.
*   **Status Indication**: Exits with a non-zero status code if significant drift is detected, suitable for CI/CD or monitoring scripts.

## Installation
To build the utility, ensure you have Go (version 1.16 or higher) installed.

1.  Navigate to the `nightly-chronal-drift-detect` directory:
    ```bash
    cd go-utils/nightly-chronal-drift-detect
    ```
2.  Build the executable:
    ```bash
    go build -o nightly-chronal-drift-detect src/main.go
    ```
    This will create an executable named `nightly-chronal-drift-detect` in the current directory.

## Usage
Run the utility by providing one or more URLs of your 'time-beacons' as command-line arguments.

```bash
./nightly-chronal-drift-detect <beacon_url_1> [beacon_url_2 ...]
```

**Example:**
```bash
./nightly-chronal-drift-detect https://www.google.com https://www.github.com https://www.example.com
```

### Output

```
Initiating Chronal Drift Scan...
Local Chronometer: Mon, 02 Jan 2023 15:04:05 GMT (UTC)
----------------------------------------
----------------------------------------
Chronal Drift Report:
  [OK] Beacon https://www.google.com: Drift -123.456ms
  [OK] Beacon https://www.github.com: Drift +50.123ms
  [ERROR] Beacon https://unreachable-beacon.com: failed to reach beacon https://unreachable-beacon.com: Get "https://unreachable-beacon.com": dial tcp: lookup unreachable-beacon.com: no such host

All time-beacons appear synchronized within acceptable temporal parameters.
```

If significant drift (currently defined as `> 1 second`) is detected on any beacon, a warning will be printed, and the utility will exit with status code `1`.

```
...
  [OK] Beacon https://www.drifting-server.com: Drift +5s

Warning: Significant chronal drift detected on one or more beacons. Temporal integrity may be compromised!
```

## Development

### Running Tests
To run the automated tests, navigate to the utility's root directory and execute:

```bash
go test ./tests/...
```
