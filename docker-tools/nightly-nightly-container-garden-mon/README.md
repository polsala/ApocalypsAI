# Nightly Container Garden Monitor

The ApocalypsAI Nightly Integrator presents the "Container Garden Monitor"! This whimsical utility treats your Docker containers like precious plants in a post-apocalyptic garden. It checks their vital signs – are they running ("watered"), consuming resources responsibly ("fed"), and free of critical errors ("blooming")? Get a quick, charming overview of your container ecosystem's health.

## Features

*   **Container Discovery**: Automatically finds all running Docker containers.
*   **Health Check**: Verifies if containers are up and running.
*   **Resource Observation (Simulated)**: Reports on CPU and memory usage with whimsical heuristics.
*   **Log Scan**: Peeks into container logs for signs of "wilting" (errors or failures).
*   **Whimsical Reporting**: Translates technical statuses into delightful garden metaphors.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-container-garden-monitor` directory and build the image:

```bash
docker build -t container-garden-monitor .
```

### 2. Run the Monitor

To allow the monitor to interact with your Docker daemon, you need to mount the Docker socket.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-garden-monitor
```

### Example Output

```
--- Container Garden Report ---

[🌱] my-web-app (Running): Blooming beautifully! Logs are clear.
[💧] database-service (Running): Blooming beautifully! Logs are clear. A bit thirsty! High memory usage detected (simulated 85%). Consider watering it with more RAM.
[🍂] log-processor (Running): Showing some wilting leaves! Errors detected in logs.
[❌] old-dev-tool (Exited): This plant has withered. It's no longer running.
```

## Configuration (Optional)

Currently, the monitor uses default thresholds for "high" resource usage and a simple keyword scan for errors. Future versions might allow custom thresholds and keywords via environment variables or a configuration file.

## Development

The core logic is a Python script that uses the `docker-py` library. Tests use `unittest.mock` to simulate Docker daemon responses.
