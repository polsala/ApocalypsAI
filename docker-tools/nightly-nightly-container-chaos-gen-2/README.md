## Nightly Container Chaos Generator

This utility provides a Dockerized environment to simulate various chaotic scenarios within your containerized applications. It's designed to help you test the resilience and fault tolerance of your systems by injecting controlled failures.

### Features

*   **Container Resource Starvation**: Simulate CPU, memory, or disk I/O pressure.
*   **Network Disruption**: Introduce latency, packet loss, or complete network isolation.
*   **Process Termination**: Randomly kill processes within a target container.
*   **Filesystem Tampering**: Corrupt or delete files within a container.

### Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t container-chaos-gen .
    ```

2.  **Run the chaos generator:**
    The `chaos-generator.sh` script takes the following arguments:
    *   `--target-container <container_name_or_id>`: The name or ID of the container to target.
    *   `--scenario <scenario_name>`: The type of chaos to inject (e.g., `cpu-starvation`, `network-latency`, `process-kill`, `filesystem-corruption`).
    *   `--duration <seconds>`: How long the chaos should last.
    *   `--intensity <value>`: Scenario-specific intensity (e.g., CPU percentage, latency in ms, corruption probability).

    **Example:** Inject network latency into a container named `my-app` for 60 seconds with 100ms latency:
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --target-container my-app --scenario network-latency --duration 60 --intensity 100
    ```

    **Example:** Simulate CPU starvation on `my-service` for 30 seconds at 80% intensity:
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --target-container my-service --scenario cpu-starvation --duration 30 --intensity 80
    ```

### Scenarios

*   `cpu-starvation`: Uses `stress-ng` to consume CPU resources.
*   `memory-starvation`: Uses `stress-ng` to consume memory.
*   `network-latency`: Uses `tc` to add latency.
*   `network-packet-loss`: Uses `tc` to add packet loss.
*   `process-kill`: Uses `pkill` to terminate random processes.
*   `filesystem-corruption`: Uses `shred` to corrupt files (use with extreme caution!).

### Development

This utility is built using a Dockerfile and a simple bash script. The `Dockerfile` sets up a minimal environment with necessary tools like `stress-ng`, `tc`, and `pkill`.

### Testing

Tests are included to verify the functionality of the `chaos-generator.sh` script in isolation. They mock Docker commands and verify script logic.
