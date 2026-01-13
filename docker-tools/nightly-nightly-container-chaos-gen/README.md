## Nightly Container Chaos Generator

This utility is a Dockerized tool designed to inject controlled chaos into your development and testing environments by generating and running random Docker Compose configurations.

### Philosophy

Embrace the unexpected! This tool helps you discover weaknesses in your containerized applications by simulating unpredictable service interactions and failures.

### Features

*   Generates random Docker Compose files with varying numbers of services, networks, and volumes.
*   Supports common service types like web servers, databases, and message queues.
*   Randomly introduces network delays, service restarts, and resource constraints.
*   Runs generated configurations within a temporary Docker network.
*   Provides a report of the chaos introduced and any observed issues.

### Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t container-chaos-gen .
    ```

2.  **Run the chaos generator:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen
    ```
    This command will:
    *   Generate a random Docker Compose file.
    *   Start the services defined in the generated file.
    *   Introduce random chaos (e.g., network latency, service restarts).
    *   Clean up all created Docker resources upon completion.

    **Customization (Optional):**
    You can pass arguments to control the chaos:
    *   `--num-services <N>`: Specify the number of services to generate (default: 3-7).
    *   `--chaos-level <LEVEL>`: Set the intensity of chaos (e.g., `low`, `medium`, `high`; default: `medium`).

    Example with customization:
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-chaos-gen --num-services 5 --chaos-level high
    ```

### How it Works

The tool uses Python to dynamically construct a `docker-compose.yml` file. It then leverages the Docker SDK for Python to spin up these services, introduce simulated failures using `tc` (traffic control) within containers, and monitor for basic connectivity issues.

### Testing

Unit tests are included to verify the generation of valid Docker Compose files and the simulation of chaos parameters. These tests are deterministic and do not require a running Docker daemon.
