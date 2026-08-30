# Nightly Container Garden

A whimsical-yet-useful Docker-based utility to manage your local development container 'gardens'. Cultivate new projects, harvest old ones, weed out unused resources, and inspect the health of your growing containers.

## Features

*   **Grow**: Start a collection of containers defined in a `docker-compose.yml` file.
*   **Harvest**: Stop and remove a running container garden.
*   **Weed**: Prune all unused Docker system resources (images, containers, volumes, networks) to keep your system tidy.
*   **Status**: Display the current state of containers in your garden.

## Installation

First, build the `nightly-container-garden` Docker image:

```bash
docker build -t nightly-container-garden .
```

Ensure your Docker daemon is running and accessible.

## Usage

The `nightly-container-garden` utility runs as a Docker container and interacts with your host's Docker daemon. You need to mount the Docker socket to allow it to manage containers.

### Commands

*   **`garden grow [-f <compose_file>]`**: Starts the services defined in the specified `docker-compose.yml` (defaults to `docker-compose.yml` in the current directory). It will build images if necessary and run containers in detached mode.
    ```bash
    # Example: Start a garden from a custom compose file
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)":/app nightly-container-garden grow -f my-dev-stack.yml
    # Example: Start a garden from default docker-compose.yml in current directory
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)":/app nightly-container-garden grow
    ```

*   **`garden harvest [-f <compose_file>]`**: Stops and removes the services, networks, and volumes defined in the specified `docker-compose.yml`.
    ```bash
    # Example: Stop and remove a garden
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)":/app nightly-container-garden harvest -f my-dev-stack.yml
    ```

*   **`garden weed`**: Performs a global Docker system prune, removing all stopped containers, unused networks, dangling images, and optionally unused volumes.
    ```bash
    # Example: Clean up all unused Docker resources
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-garden weed
    ```

*   **`garden status [-f <compose_file>]`**: Shows the status of the services defined in the specified `docker-compose.yml`.
    ```bash
    # Example: Check the status of a garden
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$(pwd)":/app nightly-container-garden status
    ```

**Important**: The `-v "$(pwd)":/app` mount is crucial for `grow`, `harvest`, and `status` commands so that the `garden` utility can find your `docker-compose.yml` file within the container's `/app` directory.

## Example `docker-compose.yml`

See `src/docker-compose.yml.example` for a typical development stack definition.
