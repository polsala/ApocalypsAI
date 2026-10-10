# ApocalypsAI Nightly Container Compost Bin

A whimsical-yet-useful Docker utility that acts as a digital compost bin for your Docker ecosystem, automatically pruning unused containers, images, and volumes to keep your environment tidy and efficient.

## Summary

The `nightly-container-compost-bin` helps you maintain a clean Docker environment by removing old, stopped containers, dangling images, unused images, and unreferenced volumes. It's like a diligent gardener, ensuring your digital flora doesn't get overgrown with digital weeds.

## Usage

To run the Container Compost Bin, you need Docker installed and running on your host machine. The utility itself runs as a Docker container and needs access to your host's Docker daemon via the Docker socket.

1.  **Build the Docker image (optional, or use a pre-built one if available):**
    ```bash
    docker build -t apocalypsai/compost-bin .
    ```

2.  **Run the compost bin:**
    Execute the container, mounting the Docker socket. This allows the script inside the container to interact with your host's Docker daemon.

    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/compost-bin
    ```
    The `--rm` flag ensures the compost bin container itself is removed after it finishes its job.

3.  **Automate with a cron job (example):**
    For regular composting, you can schedule this command using a cron job on your host:
    ```bash
    # Run daily at 3:00 AM
    0 3 * * * docker run --rm -e COMPOST_DAYS_OLD=14 -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/compost-bin >> /var/log/compost-bin.log 2>&1
    ```

## Configuration

You can configure the pruning behavior using environment variables when running the container:

*   `COMPOST_DAYS_OLD`:
    *   **Description**: Specifies the age threshold in days for resources to be considered "old" and eligible for pruning. Resources older than this threshold will be targeted.
    *   **Default**: `7` (meaning resources older than 7 days will be pruned).
    *   **Example**: To prune resources older than 30 days:
        ```bash
        docker run --rm -e COMPOST_DAYS_OLD=30 -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/compost-bin
        ```

## What it Composts (Prunes)

The utility performs the following cleanup operations:

*   **Stopped Containers**: Removes all containers that have been stopped for longer than the `COMPOST_DAYS_OLD` threshold.
*   **Dangling Images**: Removes images that are untagged and not referenced by any container. These are typically intermediate build layers or old versions.
*   **Unused Images**: Removes images that are not associated with any container and were created longer than the `COMPOST_DAYS_OLD` threshold ago.
*   **Unused Volumes**: Removes volumes that are not associated with any container and were created longer than the `COMPOST_DAYS_OLD` threshold ago.

## Limitations

*   **Image Tag Exclusion**: Currently, there is no direct mechanism to exclude images with specific tags from being pruned. All unused images older than the specified threshold are candidates for removal. If you have images you wish to keep indefinitely, ensure they are actively used by a container or manually manage them.
*   **Network Pruning**: This utility does not prune unused Docker networks. Consider `docker network prune` if you need to clean up networks.

## Development & Testing

The `compost_bin.sh` script is a simple Bash script. Tests are implemented in `tests/test_compost_bin.sh` and use a mocked `docker` command to ensure deterministic and offline verification of the script's logic.

To run tests:
```bash
bash tests/test_compost_bin.sh
```
