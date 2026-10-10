# Nightly Container Lullaby

## Overview

The `nightly-container-lullaby` is a whimsical yet practical Docker utility designed to help you manage your containerized environments. It allows you to gracefully `stop` or `pause` specified Docker containers, ensuring they are "rested" and ready for their next operational cycle. This can be particularly useful for development environments, non-critical services, or simply to conserve system resources during off-peak hours.

## Features

*   **Graceful Operations**: Executes `docker stop` or `docker pause` commands.
*   **Multiple Containers**: Can operate on one or many containers simultaneously.
*   **Feedback**: Provides clear output on which containers were successfully acted upon and which encountered issues.
*   **Containerized**: Runs as a standalone Docker image, requiring only a Docker daemon to interact with.

## How to Build

To build the Docker image for the Container Lullaby, navigate to the utility's directory and run:

```bash
docker build -t nightly-container-lullaby .
```

## How to Use

The utility expects an operation (`stop` or `pause`) followed by a list of container names or IDs.

### Prerequisites

Ensure your Docker daemon is running and accessible from where you execute the `docker run` command. The container will mount the Docker socket to interact with the host's Docker daemon.

### Examples

#### 1. Stop a single container:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-lullaby stop my-dev-database
```

#### 2. Pause multiple containers:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-lullaby pause my-frontend-app my-backend-service
```

#### 3. Stop all containers matching a pattern (using `docker ps` and `xargs`):

```bash
docker ps -a --format "{{.Names}}" | grep "^my-dev-" | xargs docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-lullaby stop
```

**Note**: The `--rm` flag ensures the lullaby container is removed after it finishes its job. The `-v /var/run/docker.sock:/var/run/docker.sock` mount is crucial for the utility to communicate with your Docker daemon.

## How to Test

The tests for `nightly-container-lullaby` are implemented in Bash and use mocking to simulate Docker commands, ensuring deterministic and offline execution.

To run the tests, execute the following command from the utility's root directory:

```bash
bash tests/test_lullaby.sh
```

This script will run a series of tests, verifying the `lullaby.sh` script's behavior under various conditions, including successful operations, handling of non-existent containers, and error scenarios.
