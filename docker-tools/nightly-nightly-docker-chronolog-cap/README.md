# Nightly Docker Chronolog Capsule

## Summary

The `nightly-docker-chronolog-capsule` is a whimsical-yet-useful utility designed to create a "time capsule" of a running Docker container's operational state. It captures the container's standard output/error logs and specified configuration/data paths, bundling them into a timestamped `.tar.gz` archive. This is invaluable for debugging, auditing, post-mortem analysis, or simply preserving a snapshot of an application's state at a particular moment in time.

## How it Works

This utility runs as its own Docker container and interacts with the Docker daemon (via a mounted `/var/run/docker.sock`). It performs the following steps:

1.  **Retrieves Logs**: Uses `docker logs` to capture the target container's stdout and stderr.
2.  **Copies Files**: Uses `docker cp` to copy specified directories or files from the target container's filesystem.
3.  **Archives**: Bundles all captured logs and files into a single `.tar.gz` archive.
4.  **Stores**: Places the archive in a designated output directory on the host machine.

## Usage

To use the Chronolog Capsule, you need to run its Docker image, providing access to the Docker daemon and specifying the target container and an output directory.

### Build the Image

First, build the Docker image for the utility:

```bash
docker build -t nightly-docker-chronolog-capsule .
```

### Run the Capsule

Run the utility container, replacing `YOUR_CONTAINER_NAME` with the name or ID of your target container and `/path/to/host/output` with the desired directory on your host machine where the archive will be saved.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/host/output:/output \
  nightly-docker-chronolog-capsule \
  YOUR_CONTAINER_NAME /output
```

**Explanation of arguments:**

*   `--rm`: Automatically remove the container when it exits.
*   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon socket, allowing the capsule container to interact with other containers on the host.
*   `-v /path/to/host/output:/output`: Mounts a host directory into the capsule container, making the captured archive accessible on your host.
*   `nightly-docker-chronolog-capsule`: The name of the utility's Docker image.
*   `YOUR_CONTAINER_NAME`: The name or ID of the Docker container you want to capture.
*   `/output`: The *internal* path within the capsule container where the archive will be saved (this corresponds to `/path/to/host/output` on your host).

### Custom Configuration Paths

You can specify additional or custom paths to capture from the target container by passing them as extra arguments. Paths should be absolute within the target container.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /path/to/host/output:/output \
  nightly-docker-chronolog-capsule \
  YOUR_CONTAINER_NAME /output \
  /etc/nginx/nginx.conf \
  /var/www/html/index.php
```

## Development and Testing

### Local Testing

The `tests/test_chronolog_capsule.sh` script provides a comprehensive way to test the utility's core logic without needing a live Docker daemon. It uses bash functions to mock `docker` commands, ensuring deterministic and offline test execution.

To run tests:

```bash
./tests/test_chronolog_capsule.sh
```

### Test Rationale

The tests mock the `docker` command to simulate its behavior for `logs` and `cp` operations. This allows the test suite to verify the script's argument parsing, file copying logic, archiving, and cleanup without external dependencies or the need to spin up actual containers. This ensures tests are fast, reliable, and self-contained.
