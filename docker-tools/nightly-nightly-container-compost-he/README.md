# Nightly Container Compost Heap

## 🌿 Overview

In the post-apocalyptic digital wasteland, unused Docker images, stopped containers, and orphaned volumes can pile up like forgotten relics, consuming precious disk space. The `Nightly Container Compost Heap` is your automated solution to this digital clutter! It's a whimsical-yet-useful containerized utility that periodically prunes your Docker system, transforming digital debris into valuable reclaimed storage.

Think of it as a diligent digital gardener, ensuring your Docker environment remains tidy and efficient, ready for the next survival challenge.

## ✨ Features

*   **Automated Pruning**: Runs `docker system prune` at configurable intervals.
*   **Configurable Options**: Customize which Docker resources are pruned (images, volumes, networks).
*   **Containerized**: Easy to deploy and manage as a Docker container itself.
*   **Whimsical Output**: Adds a touch of charm to your system maintenance logs.

## 🚀 Usage

To run the `Nightly Container Compost Heap`, you'll need Docker installed and running. The container needs access to the Docker daemon socket to perform its pruning tasks.

### Building the Docker Image

First, build the Docker image from the provided `Dockerfile`:

```bash
docker build -t nightly-container-compost-heap .
```

### Running the Container

Run the container, mounting your Docker socket and optionally configuring the prune interval and options:

```bash
docker run -d \
  --name compost-heap \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKER_PRUNE_INTERVAL="24h" \
  -e DOCKER_PRUNE_OPTIONS="--volumes --all" \
  nightly-container-compost-heap
```

**Explanation of parameters:**

*   `-d`: Runs the container in detached mode (in the background).
*   `--name compost-heap`: Assigns a memorable name to your container.
*   `--restart unless-stopped`: Ensures the container restarts automatically if Docker restarts or the container exits unexpectedly.
*   `-v /var/run/docker.sock:/var/run/docker.sock`: **CRITICAL!** This mounts the Docker daemon's socket into the container, allowing the `prune.sh` script inside to execute `docker` commands on your host's Docker daemon.
*   `-e DOCKER_PRUNE_INTERVAL="24h"`: (Optional) Sets how often the pruning occurs. Accepts values like `1s`, `30m`, `2h`, `1d`. Defaults to `24h` (daily).
*   `-e DOCKER_PRUNE_OPTIONS="--volumes --all"`: (Optional) Passes additional options to `docker system prune`. Defaults to `--volumes --all` (prunes all unused images, containers, networks, and volumes).
    *   Common options: `--all` (remove all unused images, not just dangling ones), `--volumes` (remove all unused volumes).

### Viewing Logs

To see the compost heap in action, check its logs:

```bash
docker logs -f compost-heap
```

### Stopping the Compost Heap

When you no longer need the digital gardener, you can stop and remove it:

```bash
docker stop compost-heap
docker rm compost-heap
```

## ⚙️ Configuration

Environment variables can be used to customize the behavior of the `Nightly Container Compost Heap`:

*   `DOCKER_PRUNE_INTERVAL`: The interval between prune operations. Supported units: `s` (seconds), `m` (minutes), `h` (hours), `d` (days). Examples: `10s`, `5m`, `12h`, `7d`. Default: `24h`.
*   `DOCKER_PRUNE_OPTIONS`: Additional flags passed directly to `docker system prune -f`. Default: `--volumes --all`.

## ⚠️ Important Considerations

*   **Docker Socket Access**: Granting a container access to `/var/run/docker.sock` gives it root-level access to your Docker daemon. Ensure you trust the image and understand the implications.
*   **Pruning Behavior**: `docker system prune -f` removes *all* unused (dangling and/or stopped) containers, images, networks, and optionally volumes. Be sure this is the desired behavior for your environment. If you need more granular control, consider adjusting `DOCKER_PRUNE_OPTIONS` or manually pruning specific resources.

## 🧪 Development & Testing

Refer to `src/prune.sh` for the core logic and `tests/test_prune.sh` for how the utility is tested. The tests use mocks to simulate `docker` and `sleep` commands for deterministic, offline validation.
