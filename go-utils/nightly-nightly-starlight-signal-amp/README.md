# Nightly Starlight Signal Amplifier

The Nightly Starlight Signal Amplifier is a whimsical yet powerful Go utility designed to help you discover open network ports on a target host. Like a cosmic beacon, it sends out probes across the network, listening for the faint "starlight signals" of active services. Utilizing Go's concurrency features, it scans ports rapidly and efficiently, making it an indispensable tool for network reconnaissance in the post-apocalyptic landscape.

## Features

*   **Concurrent Scanning**: Leverages Go goroutines to scan multiple ports simultaneously for speed.
*   **Configurable Host & Port Range**: Specify any target host and a range of ports to scan.
*   **Customizable Timeout**: Set a connection timeout to prevent long waits on unresponsive ports.
*   **Clear Output**: Reports all open ports found within the specified range.

## Installation

1.  **Ensure Go is installed**: If you don't have Go, download and install it from [golang.org](https://golang.org/doc/install).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-starlight-signal-amp
    ```
3.  **Build the utility**:
    ```bash
    go build -o starlight-signal-amp src/main.go
    ```

## Usage

Run the amplifier with a target host and a port range.

```bash
./starlight-signal-amp --host <target_host> --ports <start_port>-<end_port> [--timeout <seconds>]
```

*   `--host`: The target IP address or hostname (e.g., `localhost`, `127.0.0.1`, `example.com`). Defaults to `127.0.0.1`.
*   `--ports`: The range of ports to scan, specified as `START-END` (e.g., `1-1024`, `8000-9000`). This argument is required.
*   `--timeout`: (Optional) Connection timeout in seconds. Defaults to `1` second.

### Examples

Scan common web ports on localhost:
```bash
./starlight-signal-amp --host localhost --ports 80-443
```

Scan a wider range of ports on a remote server with a 2-second timeout:
```bash
./starlight-signal-amp --host 192.168.1.1 --ports 1-65535 --timeout 2
```

Scan a specific port (e.g., 22) by providing a range of 1:
```bash
./starlight-signal-amp --host example.com --ports 22-22
```

## Development & Testing

To run the tests:

```bash
go test ./tests/...
```
