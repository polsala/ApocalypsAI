# Chaos Container Scripts

This directory contains the scripts that run inside the chaos container to introduce various types of chaos into your infrastructure.

## Files

- `chaos_orchestrator.py` - Main Python script that orchestrates chaos scenarios

## Chaos Scenarios

### Network Chaos
- Adds configurable latency to network traffic using `tc`
- Can be enabled/disabled via environment variables
- Configurable latency in milliseconds

### CPU Chaos
- Applies CPU stress using `stress-ng`
- Configurable duration
- Can be enabled/disabled via environment variables

### Random Failures
- Introduces random failures based on a probability
- Configurable failure rate (0.0 to 1.0)
- Can be enabled/disabled via environment variables

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CHAOS_DURATION` | How long chaos runs | `30m` |
| `ENABLE_NETWORK_CHAOS` | Enable network latency chaos | `true` |
| `NETWORK_LATENCY_MS` | Network latency in milliseconds | `200` |
| `ENABLE_CPU_CHAOS` | Enable CPU stress chaos | `true` |
| `CPU_STRESS_DURATION` | CPU stress duration | `10m` |
| `ENABLE_RANDOM_FAILURES` | Enable random task failures | `true` |
| `FAILURE_RATE` | Probability of random failures | `0.1` |
| `WHIMSY_LEVEL` | Whimsy level: 'low', 'medium', 'high' | `high` |

## Health Check

The container exposes a health check endpoint at `http://localhost:8080/health` that returns JSON status information.

## Usage

The chaos orchestrator is designed to run inside an ECS Fargate task and will automatically clean up after itself when terminated.
