# Nightly Container Garden Monitor

## Summary
This utility, the `nightly-container-garden-monitor`, transforms your Docker containers into a whimsical 'container garden'. It diligently checks the health and resource usage of each 'plant' (container) and provides a charming report on their 'foliage condition', 'soil nutrients', and 'water levels'. It's a fun way to keep an eye on your containerized applications!

## How it Works
1.  **Connects to Docker**: The monitor uses the Docker SDK to connect to your local Docker daemon.
2.  **Identifies Plants**: It lists all running and exited Docker containers, treating each as a unique plant in your garden.
3.  **Checks Vitality**: For running containers, it inspects their health status (if a healthcheck is configured) and gathers real-time CPU and memory usage statistics.
4.  **Generates Report**: Based on the gathered data, it assigns a whimsical 'garden status' (e.g., 'Thriving Bloom', 'Wilting Petal', 'Dormant Seed') and 'foliage condition' (e.g., 'Lush & Green', 'Thirsty Roots & Overgrown Foliage').

## Usage

### 1. Build the Docker Image
Navigate to the `nightly-container-garden-monitor` directory and build the Docker image:

```bash
docker build -t container-garden-monitor .
```

### 2. Run the Monitor
To run the monitor, you need to mount the Docker socket so it can communicate with the Docker daemon. This allows it to inspect your running containers.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-garden-monitor
```

#### Example Output
```
--- ApocalypsAI Container Garden Report ---

Plant Name: my-web-app (ID: abc1234)
  Garden Status: Thriving Bloom
  Current State: Running
  Health Check: Healthy
  Foliage Condition: Lush & Green
  Soil Nutrients (CPU): 10.50%
  Water Level (Memory): 200.00 MB / 1024.00 MB

Plant Name: database-service (ID: def5678)
  Garden Status: Wilting Petal
  Current State: Running
  Health Check: Unhealthy
  Foliage Condition: Thirsty Roots & Overgrown Foliage
  Soil Nutrients (CPU): 95.20%
  Water Level (Memory): 900.00 MB / 1024.00 MB

Plant Name: old-batch-job (ID: ghi9012)
  Garden Status: Dormant Seed (Exited)
  Current State: Exited
  Health Check: Unknown
  (Plant is not active, no live stats available)

--- End of Garden Report ---
```

## Development & Testing

### Prerequisites
-   Python 3.9+
-   `pip`
-   `docker` (Python SDK)

### Running Tests
Tests are written using `unittest` and mock the Docker client interactions to ensure determinism and offline execution.

```bash
python -m unittest tests/test_garden_monitor.py
```
