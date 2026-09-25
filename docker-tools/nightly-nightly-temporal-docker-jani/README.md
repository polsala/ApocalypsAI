# Nightly Temporal Docker Janitor

A containerized utility that periodically purges old Docker resources, simulating a temporal anomaly cleanup to keep your system tidy.

## Overview

The Temporal Docker Janitor helps maintain a clean Docker environment by removing unused containers, images, volumes, and networks. It's designed to be run as a scheduled task, ensuring your system doesn't accumulate digital debris from past temporal experiments (or just old Docker builds).

## Features

*   **Containerized**: Runs within its own Docker container, requiring only Docker to be installed on the host.
*   **Configurable**: Control which types of resources to prune using environment variables.
*   **Whimsical Output**: Enjoy a bit of temporal-themed flair with your cleanup logs.

## Usage

To run the Temporal Docker Janitor, you need to execute its Docker container and mount the Docker socket from your host. This allows the containerized script to interact with your host's Docker daemon.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  -e DOCKER_PRUNE_CONTAINERS=true \
  -e DOCKER_PRUNE_IMAGES=true \
  -e DOCKER_PRUNE_ALL_IMAGES=false \
  -e DOCKER_PRUNE_VOLUMES=false \
  -e DOCKER_PRUNE_NETWORKS=false \
  nightly-temporal-docker-janitor
```

### Environment Variables

You control the janitor's behavior using the following environment variables:

*   `DOCKER_PRUNE_CONTAINERS`: Set to `true` to prune all stopped containers. Defaults to `true`.
*   `DOCKER_PRUNE_IMAGES`: Set to `true` to prune dangling (untagged) images. Defaults to `true`.
*   `DOCKER_PRUNE_ALL_IMAGES`: Set to `true` to prune all unused images (not just dangling ones). Requires `DOCKER_PRUNE_IMAGES` to also be `true`. Defaults to `false`.
*   `DOCKER_PRUNE_VOLUMES`: Set to `true` to prune all unused volumes. **Use with caution**, as volumes often contain persistent data. Defaults to `false`.
*   `DOCKER_PRUNE_NETWORKS`: Set to `true` to prune all unused networks. Defaults to `false`.

Any variable not explicitly set to `false` will default to `true` for containers and dangling images, and `false` for volumes, networks, and all images.

## Building the Image

To build the Docker image yourself:

```bash
docker build -t nightly-temporal-docker-janitor .
```

## Scheduling

For automated cleanup, you can schedule this utility using `cron` on your host system:

```bash
# Example: Run every night at 3:00 AM
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e DOCKER_PRUNE_CONTAINERS=true -e DOCKER_PRUNE_IMAGES=true nightly-temporal-docker-janitor >> /var/log/docker-janitor.log 2>&1
```

Adjust the cron schedule and environment variables to fit your needs.
