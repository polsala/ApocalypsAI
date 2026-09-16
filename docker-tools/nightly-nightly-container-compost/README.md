# Nightly Container Compost

## Overview

The `nightly-container-compost` utility acts as a digital compost heap for your Docker environment. It helps you reclaim valuable disk space and system resources by identifying and optionally pruning stale, exited containers, dangling images, unused volumes, and build cache.

Think of it as a friendly scavenger bot, tidying up the digital wasteland of your Docker daemon, turning forgotten bits into fertile ground for new deployments.

## Features

*   **Stale Container Detection**: Identifies stopped containers older than a specified age.
*   **Dangling Image Detection**: Finds images that are not tagged and not associated with any container.
*   **Dangling Volume Detection**: Locates volumes not currently used by any container.
*   **Build Cache Pruning**: Cleans up unused build cache layers.
*   **Dry Run Mode**: Safely preview what will be composted without making any changes.
*   **Automated Pruning**: Automatically removes identified items when not in dry-run mode.

## Usage

This utility is designed to run as a Docker container, mounting the host's Docker socket to interact with the Docker daemon.

### Prerequisites

*   Docker installed and running on your host machine.

### Running the Compost Heap

To run the utility, execute the following Docker command. The `--dry-run` flag is highly recommended for your first few runs to see what will be affected.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-container-compost:latest \
  [--dry-run] [--container-age-hours <hours>] [--no-prune-containers] [--no-prune-images] [--no-prune-volumes] [--no-prune-build-cache]
```

**Example: Dry run to see what can be composted (default container age: 24 hours)**

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-container-compost:latest \
  --dry-run
```

**Example: Compost containers older than 72 hours and prune all other items**

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-container-compost:latest \
  --container-age-hours 72
```

**Example: Only prune dangling images and volumes, skip containers and build cache**

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-container-compost:latest \
  --no-prune-containers --no-prune-build-cache
```

### Options

*   `--dry-run`: (Optional) Perform a dry run. No items will be removed, only reported.
*   `--container-age-hours <hours>`: (Optional) Specify the minimum age in hours for stopped containers to be considered stale. Defaults to `24` hours.
*   `--no-prune-containers`: (Optional) Skip pruning of stale containers.
*   `--no-prune-images`: (Optional) Skip pruning of dangling images.
*   `--no-prune-volumes`: (Optional) Skip pruning of dangling volumes.
*   `--no-prune-build-cache`: (Optional) Skip pruning of build cache.

## Building the Image

To build the Docker image for this utility:

```bash
docker build -t nightly-container-compost:latest .
```

## Development and Testing

See `tests/test_compost.sh` for how the utility is tested. The `src/compost.sh` script is designed to be testable by allowing `docker_cmd` to be overridden for mocking purposes.
