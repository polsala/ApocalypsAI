# Nightly Resource Scavenger

In the post-apocalyptic digital wasteland, containers can become feral, hoarding precious CPU cycles and memory, or simply lying dormant like forgotten relics. The `Nightly Resource Scavenger` is your vigilant companion, a containerized utility designed to patrol your Docker host, identifying and reporting on containers that are either consuming excessive resources or have been stopped for an unacceptably long time.

Keep your container ecosystem lean, efficient, and ready for whatever the digital frontier throws at it!

## Features

*   **Resource Hog Detection**: Flags running containers exceeding configurable CPU and memory usage thresholds.
*   **Stale Container Identification**: Pinpoints stopped containers that have been inactive for more than a specified number of days.
*   **Configurable Thresholds**: Customize CPU, memory, and stale-day thresholds to fit your operational needs.
*   **Containerized Execution**: Runs as a Docker container itself, requiring only Docker to be installed on the host.

## Usage

1.  **Ensure Docker is Running**: This utility requires the Docker daemon to be active on your host machine.

2.  **Run the Scavenger**: Execute the `run_scavenger.sh` script. This script will build the Docker image (if not already built) and then run the scavenger container, mounting your host's Docker socket (`/var/run/docker.sock`) to allow it to inspect other containers.

    ```bash
    ./src/run_scavenger.sh
    ```

    The output will be a report detailing any identified resource-hungry or stale containers.

### Customizing Thresholds

You can pass arguments to `run_scavenger.sh` to customize the thresholds:

*   `--cpu-threshold <PERCENTAGE>`: Set the CPU usage percentage above which a running container is considered resource-hungry (default: `80`).
*   `--mem-threshold <PERCENTAGE>`: Set the memory usage percentage above which a running container is considered resource-hungry (default: `80`).
*   `--stale-days <DAYS>`: Set the number of days after which a stopped container is considered stale (default: `7`).

**Example: Identify containers with >50% CPU, >60% Memory, or stopped for >3 days**

```bash
./src/run_scavenger.sh --cpu-threshold 50 --mem-threshold 60 --stale-days 3
```

## Development and Testing

### Building the Docker Image Manually

If you wish to build the Docker image without running the scavenger immediately:

```bash
docker build -t apocalypsai/nightly-resource-scavenger .
```

### Running Tests

The `tests/test_scavenger.sh` script provides automated, deterministic tests for the core logic of the `scavenge.sh` script. It uses mocked `docker` and `date` commands to simulate container states and resource usage without requiring a live Docker daemon.

To run the tests:

```bash
./tests/test_scavenger.sh
```

This will execute a series of checks against the `scavenge.sh` script's output under various mocked scenarios and threshold configurations.
