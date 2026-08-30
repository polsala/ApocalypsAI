# nightly-temporal-drift-sync

A whimsical-yet-useful Go-based distributed service designed to collect "temporal drift" reports from various "chronometer" nodes across the ApocalypsAI network. It then calculates and provides a real-time, consensus-based temporal offset, helping to stabilize the fabric of spacetime (or at least, your distributed system's metrics).

## How it Works

The `nightly-temporal-drift-sync` service acts as a central hub for temporal data.
- **Report Drift**: Nodes (or "chronometers") send their observed temporal drift values to the service via a POST request. Each report includes a unique `node_id` and a `drift_value` (a floating-point number representing the deviation).
- **Consensus Calculation**: The service maintains the latest drift value for each active node. Upon request, it calculates a "consensus drift" by averaging all reported values. This provides a harmonized view of temporal stability.
- **Concurrency**: Built with Go's concurrency primitives, it can handle multiple drift reports and consensus queries simultaneously.

## Usage

### 1. Build the Service

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/go-utils/nightly-temporal-drift-sync
go build -o temporal-drift-sync src/main.go
```

### 2. Run the Service

```bash
./temporal-drift-sync
# Service will start on port 8080 by default.
# You can specify a different port: PORT=8081 ./temporal-drift-sync
```

### 3. Report Temporal Drift

Send a POST request with a JSON payload to `/report-drift`.

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"node_id": "chronometer-alpha", "drift_value": 0.15}' \
     http://localhost:8080/report-drift

curl -X POST -H "Content-Type: application/json" \
     -d '{"node_id": "chronometer-beta", "drift_value": -0.05}' \
     http://localhost:8080/report-drift

curl -X POST -H "Content-Type: application/json" \
     -d '{"node_id": "chronometer-gamma", "drift_value": 0.20}' \
     http://localhost:8080/report-drift
```

### 4. Get Consensus Temporal Offset

Send a GET request to `/consensus-drift`.

```bash
curl http://localhost:8080/consensus-drift
# Example response: {"consensus_drift": 0.1}
```

## Development

### Running Tests

```bash
cd ApocalypsAI/go-utils/nightly-temporal-drift-sync
go test ./tests/...
```
