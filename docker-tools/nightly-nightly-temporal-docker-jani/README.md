# Nightly Temporal Docker Janitor

The digital detritus of forgotten containers and orphaned images can accumulate, slowing down your development timelines and consuming precious disk space. Fear not, for the Nightly Temporal Docker Janitor is here to sweep away the temporal anomalies of your Docker environment!

This whimsical-yet-useful utility is a self-contained Docker image designed to prune unused and dangling Docker resources (images, containers, volumes, networks) from your host system. It operates like a temporal void-sweeper, ensuring your Docker realm remains pristine and efficient.

## Features

*   **Containerized Cleanup**: Runs as a Docker container, requiring only Docker to be installed on your host.
*   **Comprehensive Pruning**: Utilizes `docker system prune -a -f --volumes` to remove all unused and dangling images, containers, volumes, and networks.
*   **Scheduled Operations**: Easily integrated into cron jobs or CI/CD pipelines for automated, regular cleanups.
*   **Whimsical Output**: Provides a touch of temporal flair to its cleanup reports.

## Usage

### 1. Build the Docker Image

First, you need to build the `nightly-temporal-docker-janitor` image. Navigate to the utility's directory and run:

```bash
docker build -t nightly-temporal-docker-janitor .
```

### 2. Run the Janitor

To run the janitor, you need to mount the Docker socket from your host into the container. This allows the janitor container to interact with the Docker daemon on your host and perform the cleanup.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-temporal-docker-janitor
```

*   `--rm`: Automatically remove the container when it exits.
*   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon socket, granting the container access to manage Docker resources on the host. **Be aware of the security implications of mounting the Docker socket.**

### 3. Schedule with Cron (Example)

For automated nightly cleanups, you can add an entry to your system's cron table.

1.  Open your crontab for editing:
    ```bash
    crontab -e
    ```
2.  Add a line like this to run the janitor every night at 3:00 AM:
    ```cron
    0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-temporal-docker-janitor >> /var/log/docker-janitor.log 2>&1
    ```
    (Ensure the `nightly-temporal-docker-janitor` image is already built and available on your host.)

## How it Works

The `janitor.sh` script inside the container simply executes `docker system prune -a -f --volumes`. This command removes:
*   All stopped containers
*   All dangling images
*   All unused images (not just dangling ones)
*   All dangling build cache
*   All unused networks
*   All unused volumes

The `-f` flag forces the operation without a confirmation prompt, which is suitable for automated tasks.

## Security Considerations

Mounting `/var/run/docker.sock` into a container effectively gives that container root access to your Docker host. Only run this utility if you trust its contents and understand the implications.
