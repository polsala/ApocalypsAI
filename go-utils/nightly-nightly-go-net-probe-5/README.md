## nightly-go-net-probe

A whimsical yet useful Go utility for concurrently probing network endpoints. It checks for service availability and measures latency, providing a quick overview of your network's health.

### Philosophy

Inspired by the need for a robust and concurrent network checking tool, this utility leverages Go's excellent concurrency primitives to efficiently scan multiple targets.

### Usage

To run the probe, you need to provide a list of target hosts and ports. The utility will then concurrently send TCP connection attempts to each target and report the results.

```bash
./nightly-go-net-probe <host1>:<port1> <host2>:<port2> ...
```

**Example:**

```bash
./nightly-go-net-probe google.com:80 example.com:443 localhost:8080
```

### Output

The output will show each target, whether it was reachable, and the time it took to establish a connection (latency).

```
Target: google.com:80 | Reachable: true | Latency: 15ms
Target: example.com:443 | Reachable: true | Latency: 32ms
Target: localhost:8080 | Reachable: false | Error: connection refused
```

### Building

Ensure you have Go installed. Then, navigate to the `go-utils/nightly-go-net-probe/src` directory and run:

```bash
go build -o ../nightly-go-net-probe
```

This will create an executable in the root of the utility's directory.

### Testing

To run the included tests, navigate to the `go-utils/nightly-go-net-probe` directory and run:

```bash
go test ./...
```
