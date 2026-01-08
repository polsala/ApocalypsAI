## Temporal Sync Checker

A whimsical yet useful utility to ensure that simulated temporal nodes are in sync. In the chaotic aftermath of temporal anomalies, maintaining synchronized time across different pockets of reality is crucial for stability. This tool helps verify that.

### Installation

```bash
npm install -g @apocalypsai/temporal-sync-checker
```

### Usage

```bash
temporal-sync-checker --nodes <node1_url> <node2_url> ... [--tolerance <seconds>]
```

**Arguments:**

*   `--nodes`: A space-separated list of URLs for the simulated temporal nodes to check.
*   `--tolerance`: (Optional) The maximum acceptable difference in seconds between node times. Defaults to 5 seconds.

### Example

```bash
temporal-sync-checker --nodes http://node1.temporal.local http://node2.temporal.local --tolerance 10
```

This command will check if the time difference between `node1.temporal.local` and `node2.temporal.local` is within 10 seconds. If the difference exceeds the tolerance, it will report the discrepancy.

### How it Works

The utility makes a simple HTTP GET request to each specified node. It assumes each node will respond with a JSON payload containing a `timestamp` field (in milliseconds since epoch). It then calculates the difference between the current system time and the timestamp reported by each node, and compares these differences across all nodes.

### Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.
