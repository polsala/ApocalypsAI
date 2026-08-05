# Nightly Cosmic Dust Sweeper

## 🌌 Overview

The `nightly-cosmic-dust-sweeper` is a whimsical-yet-useful containerized utility designed to keep your Docker environment pristine. It periodically sweeps away the accumulated 'cosmic dust' – unused Docker images, stopped containers, and dangling volumes – ensuring your host remains tidy and optimized for the next grand cosmic event (or just your next development sprint).

This tool is built as a Docker image, allowing it to be easily deployed and scheduled via cron, systemd timers, or even as a Kubernetes CronJob, by mounting the host's Docker socket.

## ✨ Features

*   **Comprehensive Pruning**: Utilizes `docker system prune --all --force` to remove all stopped containers, all unused images (not just dangling ones), and all unused networks.
*   **Volume Management**: Optionally includes unused volumes in the sweep.
*   **Dry Run Mode**: Allows you to see what would be removed without making any actual changes.
*   **Containerized**: Runs as a self-contained Docker image, minimizing host dependencies.

## 🚀 Usage

### 1. Build the Docker Image

Navigate to the utility's directory and build the image:

```bash
docker build -t nightly-cosmic-dust-sweeper .
```

### 2. Run the Sweeper

To run the sweeper, you need to mount your host's Docker socket (`/var/run/docker.sock`) into the container so it can interact with the Docker daemon.

#### Basic Run (with volumes, actual sweep):

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-cosmic-dust-sweeper
```

#### Dry Run (see what would be removed):

```bash
docker run --rm -e DRY_RUN="true" -v /var/run/docker.sock:/var/run/docker.sock nightly-cosmic-dust-sweeper
```

#### Run without Pruning Volumes:

```bash
docker run --rm -e INCLUDE_VOLUMES="false" -v /var/run/docker.sock:/var/run/docker.sock nightly-cosmic-dust-sweeper
```

### 3. Configuration

The sweeper can be configured using environment variables:

*   `DRY_RUN`: Set to `"true"` to perform a dry run. No actual changes will be made. Defaults to `"false"`.
*   `INCLUDE_VOLUMES`: Set to `"false"` to skip pruning unused volumes. Defaults to `"true"`.

### 4. Scheduling (Example: Cron Job)

For automated, periodic cleanup, you can schedule the container to run using a cron job. Edit your crontab (`crontab -e`) and add a line like this to run the sweeper daily at 3:00 AM:

```cron
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-cosmic-dust-sweeper > /var/log/cosmic-dust-sweeper.log 2>&1
```

Or, for a dry run weekly:

```cron
0 4 * * 0 docker run --rm -e DRY_RUN="true" -v /var/run/docker.sock:/var/run/docker.sock nightly-cosmic-dust-sweeper > /var/log/cosmic-dust-sweeper-dry-run.log 2>&1
```

Remember to adjust the schedule and logging as per your needs.

## ⚠️ Important Considerations

*   **Permissions**: The container needs access to `/var/run/docker.sock`, which grants it full control over your Docker daemon. Use with caution and ensure you understand the implications.
*   **Data Loss**: `docker system prune --all --force --volumes` is an aggressive command. While it targets *unused* resources, always ensure you don't have critical stopped containers, untagged images, or unreferenced volumes that you wish to keep before running this in production without a dry run.

May your Docker realm remain ever clean and efficient!
