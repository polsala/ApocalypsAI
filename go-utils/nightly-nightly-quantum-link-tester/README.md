# Nightly Quantum Link Tester

## Overview

The `nightly-quantum-link-tester` is a whimsical-yet-useful Go CLI utility designed to assess the 'quantum entanglement' of your network links. It concurrently pings multiple specified hosts, measures their average latency and jitter, and synthesizes this data into a single 'Quantum Entanglement Score'. A higher score indicates a more stable and responsive connection, suggesting a stronger, more 'entangled' link to the cosmic network.

## Features

*   **Concurrent Pinging**: Tests multiple hosts simultaneously using Go's goroutines.
*   **Latency & Jitter Measurement**: Provides average round-trip time (RTT) and standard deviation (jitter) for each target.
*   **Quantum Entanglement Score**: A proprietary metric (higher is better!) that reflects the overall stability and performance of your connection to a given host.
*   **Configurable**: Specify hosts and ping count.

## Installation

1.  **Prerequisites**: Ensure you have Go (1.16+) installed.
2.  **Clone the repository** (if not already part of ApocalypsAI):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/go-utils/nightly-quantum-link-tester
    ```
3.  **Build the utility**:
    ```bash
    go build -o quantum-link-tester src/main.go
    ```

## Usage

Run the executable with a list of hosts to test:

```bash
./quantum-link-tester --hosts google.com,github.com,example.com --count 5
```

### Arguments:

*   `--hosts <comma-separated-list>`: Required. A list of hostnames or IP addresses to ping.
*   `--count <number>`: Optional. The number of pings to send to each host. Default is 4.
*   `--timeout <duration>`: Optional. Timeout for each ping attempt (e.g., `1s`, `500ms`). Default is `1s`.

### Example Output:

```
🌌 Initiating Quantum Link Test...

Testing entanglement with google.com (5 pings, timeout 1s):
  Avg Latency: 25.34 ms
  Jitter: 2.11 ms
  Quantum Entanglement Score: 37.6

Testing entanglement with github.com (5 pings, timeout 1s):
  Avg Latency: 80.12 ms
  Jitter: 5.45 ms
  Quantum Entanglement Score: 11.7

Testing entanglement with example.com (5 pings, timeout 1s):
  Avg Latency: 150.01 ms
  Jitter: 10.23 ms
  Quantum Entanglement Score: 6.3

✨ Quantum Link Test Complete. May your connections be ever entangled!
```

## Quantum Entanglement Score Interpretation

The score is calculated as `1000 / (AvgLatencyMs + JitterMs + 1)`. 

*   **Higher Score (e.g., > 30)**: Indicates a strong, stable, and highly 'entangled' connection. Your signals are traversing the cosmic fabric with minimal distortion.
*   **Medium Score (e.g., 10-30)**: A decent connection, but there might be some minor temporal distortions or cosmic interference. Room for improvement in entanglement.
*   **Lower Score (e.g., < 10)**: Your link is experiencing significant temporal drift or quantum decoherence. Consider re-aligning your network's cosmic receptors.

## Development

To run tests:

```bash
go test ./tests
```
