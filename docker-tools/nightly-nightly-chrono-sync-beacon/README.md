# Nightly Chrono-Sync Beacon

## Summary

The `nightly-chrono-sync-beacon` is a whimsical-yet-useful Dockerized utility designed to ensure temporal consistency across your containerized survival infrastructure. It synchronizes the system clocks of specified Docker containers with the host's current UTC time, preventing clock drift that can lead to data inconsistencies, logging issues, and authentication failures in distributed systems.

## How it Works

This utility runs as a Docker container that requires access to the host's Docker daemon (by mounting `/var/run/docker.sock`). It takes a list of target container names or IDs as arguments. For each target, it executes a `date -u -s` command inside the container, setting its clock to the current UTC time of the host system (as observed by the utility container).

## Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t nightly-chrono-sync-beacon .
    ```

2.  **Run the utility:**
    You need to provide the names or IDs of the containers whose clocks you want to synchronize.
    The utility container must mount the Docker socket (`/var/run/docker.sock`) to interact with other containers.

    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-chrono-sync-beacon <container_name_1> [container_name_2 ...]
    ```

    **Example:**
    First, start a couple of dummy containers:
    ```bash
    docker run -d --name survival-pod-alpha busybox sleep 3600
    docker run -d --name resource-processor-beta busybox sleep 3600
    ```

    Now, run the Chrono-Sync Beacon to synchronize their clocks:
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-chrono-sync-beacon survival-pod-alpha resource-processor-beta
    ```

    The output will show the synchronization status for each container.

## Requirements

*   Docker installed and running on the host system.
*   The target containers must have the `date` command available (most base images like `busybox` or `alpine` include it).
*   The user running the `docker run` command must have permissions to access `/var/run/docker.sock` (e.g., be part of the `docker` group).

## Development & Testing

See `tests/test_chrono_sync.sh` for how to run automated tests and verify functionality.
