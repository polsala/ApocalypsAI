# Nightly Container Garden Monitor

The Nightly Container Garden Monitor transforms your bustling Docker environment into a serene, yet informative, digital garden. Each running container is represented as a unique plant, its vitality reflecting the container's health and status. Quickly spot wilting services or thriving applications at a glance!

## Features

-   **Whimsical Visualization**: See your containers as a vibrant ASCII art garden.
-   **Health at a Glance**: Plant appearance changes based on container status (running, exited, unhealthy).
-   **Simple Integration**: Runs as a Docker container, connecting to your Docker daemon.

## Usage

1.  **Ensure Docker is running**: This utility needs access to the Docker daemon.
2.  **Run the monitor**: 
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        polsala/nightly-container-garden-monitor
    ```
    (Note: `polsala/nightly-container-garden-monitor` is a placeholder for the actual image name once built and pushed.)

    This command mounts your Docker socket into the monitor container, allowing it to communicate with your Docker daemon. The `--rm` flag ensures the monitor container is removed after it exits.

## Garden Legend

-   🌱 **Thriving Sprout**: Container is `running` and `healthy` (if health check is configured).
-   🌿 **Vigorous Vine**: Container is `running` and `healthy` (if no health check, or health check passes).
-   🥀 **Wilting Blossom**: Container is `running` but `unhealthy`.
-   💀 **Withered Root**: Container is `exited` or `dead`.
-   🐛 **Pest Infestation**: Container is `restarting` or in a problematic state.

## Development

To build the Docker image locally:

```bash
docker build -t nightly-container-garden-monitor .
```

To run the local image:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
    nightly-container-garden-monitor
```

## Configuration

Currently, the monitor has no external configuration options. It automatically detects and displays all running and exited containers.
