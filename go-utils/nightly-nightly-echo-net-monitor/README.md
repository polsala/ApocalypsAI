# Nightly Echo Net Monitor

The digital realm is not always silent. Sometimes, faint whispers, temporal distortions, and echoes of impending network doom can be detected by those attuned to the network fabric. The `Nightly Echo Net Monitor` is your vigilant sentinel, a Go-based utility designed to listen for these subtle anomalies across your critical network pathways.

It concurrently probes hosts for latency, consults the ancient scrolls of DNS for domain stability, and knocks on the digital gates of HTTP endpoints to ensure they respond harmoniously. When it detects a shimmer in the fabric or a discordant echo, it reports it, guiding you to potential instabilities before they manifest into full-blown digital cataclysms.

## Features

*   **Concurrent Probing**: Utilizes Go's goroutines to check multiple hosts, DNS entries, and HTTP endpoints simultaneously for efficiency.
*   **Latency Detection**: Pings specified hosts (via TCP dial) and flags "temporal distortions" if latency exceeds a defined threshold.
*   **DNS Scroll Verification**: Performs DNS lookups for domains, ensuring the "ancient scrolls" are readable and, optionally, that they point to expected IPs.
*   **HTTP Gatekeeper**: Makes HTTP GET requests to URLs, verifying the "digital gates" respond with the expected status code.
*   **Whimsical Reporting**: Translates technical network states into evocative, apocalyptic-themed messages.
*   **Self-Contained**: A single Go executable, easy to deploy and run.

## How to Run

1.  **Save the code**: Place the `main.go` file into a directory named `nightly-echo-net-monitor/src/`.
2.  **Navigate**: Open your terminal and navigate to the `nightly-echo-net-monitor/src/` directory.
3.  **Run**: Execute the Go program:
    ```bash
    go run main.go
    ```

    The utility will perform its checks and print a summary of the network's state, highlighting any detected echoes or distortions.

## Configuration (Hardcoded for simplicity)

For this version, the hosts, DNS domains, and HTTP endpoints to monitor, along with their thresholds and expected values, are hardcoded directly within `src/main.go`.

**Example checks defined in `main.go`:**

```go
	hostChecks := []HostCheck{
		{Address: "8.8.8.8", ThresholdMs: 100},
		{Address: "1.1.1.1", ThresholdMs: 100},
	}

	dnsChecks := []DNSCheck{
		{Domain: "google.com", ExpectedIPs: []string{"142.250.190.142"}}, // Example IP, might change
		{Domain: "cloudflare.com"}, // No specific IP expected, just resolve
	}

	httpChecks := []HTTPCheck{
		{URL: "https://www.google.com", ExpectedStatus: 200, TimeoutMs: 5000},
		{URL: "https://www.github.com", ExpectedStatus: 200, TimeoutMs: 5000},
	}
```

To customize the monitoring targets, you would need to edit these slices directly in `src/main.go`.

## Development & Testing

To run the tests:

1.  **Save the code**: Place `main.go` in `nightly-echo-net-monitor/src/` and `test_main.go` in `nightly-echo-net-monitor/tests/`.
2.  **Navigate**: Open your terminal and navigate to the `nightly-echo-net-monitor/src/` directory (where `main.go` is).
3.  **Run Tests**: Execute the Go test command:
    ```bash
    go test ../tests/test_main.go main.go
    ```
    This command runs the tests defined in `test_main.go` against the `main.go` source file, utilizing the mock functions to ensure deterministic and offline testing.

## Contributing

Feel free to enhance the monitor's capabilities, add more whimsical reporting, or integrate external configuration methods (e.g., JSON file parsing) to make it even more adaptable to the ever-shifting network landscape.
