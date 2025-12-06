# Nightly Docker Wasteland Weeder

## Summary

The `nightly-docker-wasteland-weeder` is a whimsical-yet-useful containerized utility designed to help you maintain a clean and efficient Docker environment. It identifies and prunes unused Docker images, stopped containers, dangling volumes, and build cache, preventing them from accumulating and consuming valuable disk space in your digital wasteland.

## Features

*   **Dry Run Mode**: See what resources would be pruned without actually removing anything.
*   **Selective Pruning**: Choose to prune only images, containers, volumes, or build cache.
*   **Force Mode**: Skip confirmation prompts for automated cleanup.
*   **Containerized**: Runs as a Docker image, ensuring consistent behavior across different hosts.

## How to Build

To build the `nightly-docker-wasteland-weeder` Docker image, navigate to the utility's directory and run:

```bash
docker build -t nightly-docker-wasteland-weeder .
```

## How to Run

The utility needs access to the Docker daemon to perform its operations. This is typically achieved by mounting the Docker socket (`/var/run/docker.sock`) into the container.

### Dry Run (Recommended First Step)

To see what resources would be pruned without making any changes:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --dry-run
```

### Prune All Unused Resources (Interactive)

This will prompt for confirmation before removing stopped containers, dangling images, unused volumes, and build cache:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --all
```

### Force Prune All Unused Resources (Non-interactive)

This will remove all unused resources without asking for confirmation:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --force --all
```

### Selective Pruning

You can specify which types of resources to prune:

*   **Images only**: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --force --images`
*   **Containers only**: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --force --containers`
*   **Volumes only**: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --force --volumes`
*   **Build Cache only**: `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-wasteland-weeder --force --build-cache`

### Help Message

To display the usage instructions:

```bash
docker run --rm nightly-docker-wasteland-weeder --help
```

## Automated Tests

The utility includes a comprehensive test suite to ensure its functionality. The tests use mocks for Docker commands to ensure determinism and offline execution.

To run the tests, execute the `test_weeder.sh` script directly:

```bash
bash tests/test_weeder.sh
```
