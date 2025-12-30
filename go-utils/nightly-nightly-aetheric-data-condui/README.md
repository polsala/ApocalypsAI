# Nightly Aetheric Data Conduit

## Summary

The `nightly-aetheric-data-conduit` is a whimsical-yet-useful TCP proxy written in Go. It's designed to simulate unreliable network conditions by introducing configurable 'aetheric' anomalies such as artificial delays, packet loss, and data corruption. This tool is invaluable for testing the resilience and error-handling capabilities of your applications against real-world network flakiness.

## Features

*   **Configurable Delay**: Add a fixed or random delay to data packets.
*   **Packet Loss Simulation**: Randomly drop a percentage of data packets.
*   **Data Corruption**: Randomly alter bytes within data packets.
*   **Concurrent Handling**: Efficiently proxies multiple client connections using Go's concurrency model.
*   **Simple CLI**: Easy to configure via command-line flags.

## Usage

### Build

To build the conduit, navigate to the `src` directory and run:

```bash
go build -o aetheric-conduit main.go
```

This will produce an executable named `aetheric-conduit`.

### Run

Run the proxy with the desired configuration. For example, to listen on port `8080` and proxy to `example.com:80` with a 100ms delay and 5% packet loss:

```bash
./aetheric-conduit \
  --listen-port 8080 \
  --target-host example.com \
  --target-port 80 \
  --delay-ms 100 \
  --loss-rate 0.05 \
  --corruption-rate 0.01
```

**Command-line Flags:**

*   `--listen-port <port>`: The local port the conduit will listen on (e.g., `8080`). (Required)
*   `--target-host <host>`: The target hostname or IP address to proxy to (e.g., `api.example.com`). (Required)
*   `--target-port <port>`: The target port to proxy to (e.g., `443`). (Required)
*   `--delay-ms <milliseconds>`: Average delay to introduce for each data chunk in milliseconds (default: `0`).
*   `--loss-rate <rate>`: Probability of dropping a data chunk (0.0 to 1.0, default: `0.0`).
*   `--corruption-rate <rate>`: Probability of corrupting a single byte within a data chunk (0.0 to 1.0, default: `0.0`).
*   `--buffer-size <bytes>`: Size of the buffer used for copying data (default: `4096`).

### Example Scenario

Imagine you have a client application that connects to a backend service on `backend.mycorp.com:5000`. To test how your client handles network issues, you can run the conduit:

```bash
./aetheric-conduit \
  --listen-port 5001 \
  --target-host backend.mycorp.com \
  --target-port 5000 \
  --delay-ms 250 \
  --loss-rate 0.10
```

Now, configure your client application to connect to `localhost:5001` instead of `backend.mycorp.com:5000`. All traffic will pass through the conduit, experiencing simulated delays and packet loss.
