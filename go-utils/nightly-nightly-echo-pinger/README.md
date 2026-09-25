# Nightly Echo-Pinger

In the desolate expanse, reliable communication is paramount. The Nightly Echo-Pinger is a Go-powered CLI utility designed to send out concurrent 'echoes' (pings) to a list of network targets, reporting back on their responsiveness and latency. It helps survivors quickly assess network health and identify silent zones, ensuring your vital data packets don't vanish into the void.

## Features

*   **Concurrent Pinging**: Utilizes Go's goroutines to ping multiple targets simultaneously for rapid assessment.
*   **Latency Reporting**: Provides round-trip time for successful pings.
*   **Reachability Status**: Clearly indicates whether a target is reachable or silent.
*   **Flexible Input**: Accepts targets directly as command-line arguments or from a file.

## Installation

1.  Ensure you have Go (1.16 or newer) installed.
2.  Clone the ApocalypsAI repository.
3.  Navigate to the `go-utils/nightly-echo-pinger` directory:
    ```bash
    cd go-utils/nightly-echo-pinger
    ```
4.  Build the executable:
    ```bash
    go build -o nightly-echo-pinger src/main.go
    ```
5.  (Optional) Move the executable to your PATH:
    ```bash
    sudo mv nightly-echo-pinger /usr/local/bin/
    ```

## Usage

### Ping targets directly from command line:

```bash
./nightly-echo-pinger google.com 8.8.8.8 localhost
```

### Ping targets from a file:

Create a file named `targets.txt` (or any name) with one target per line:

```
# targets.txt
google.com
192.168.1.1
example.com
unknown.host
```

Then run:

```bash
./nightly-echo-pinger -f targets.txt
```

### Example Output:

```
📡 Initiating Echo-Location Scan...

[google.com] Echo Received! Latency: 25.34 ms
[8.8.8.8] Echo Received! Latency: 12.87 ms
[localhost] Echo Received! Latency: 0.05 ms
[unknown.host] Silence Detected. Target unreachable. (exit status 1)

Scan Complete. May your signals always find their way.
```

## Development

To run tests:

```bash
go test ./tests/...
```
