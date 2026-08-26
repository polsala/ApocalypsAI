# Nightly Docker Compost Bin

## 🌿 Overview

The `nightly-docker-compost` is a whimsical, yet highly practical, containerized utility designed to keep your Docker environment pristine. Like a diligent digital gardener, it prunes away the accumulated digital detritus: unused images, stopped containers, and dangling volumes. This helps reclaim disk space and maintain a healthy, efficient Docker setup.

It runs as a Docker container itself, connecting to the host's Docker daemon to perform its cleanup tasks. This makes it easy to deploy and schedule, for example, as a nightly cron job.

## 🚀 How It Works

The utility's Docker container includes the `docker` CLI. When run, it mounts the host's Docker socket (`/var/run/docker.sock`) to interact with the host's Docker daemon. It then executes `docker prune` commands based on the provided arguments or environment variables.

## 🛠️ Usage

To run the Docker Compost Bin, you need to execute its container with access to your host's Docker socket. This is typically done with the `-v /var/run/docker.sock:/var/run/docker.sock` flag.

### Build the image (optional, if not using a pre-built one):

```bash
docker build -t nightly-docker-compost .
```

### Run the utility:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-compost [OPTIONS]
```

### Options:

- `--all` or `-a`: Prune all unused images (not just dangling ones), stopped containers, and dangling volumes. This is the default behavior if no specific prune options are given.
- `--images` or `-i`: Prune only dangling and unused images.
- `--containers` or `-c`: Prune only stopped containers.
- `--volumes` or `-v`: Prune only dangling volumes.
- `--dry-run` or `-d`: Simulate the pruning process without actually deleting anything. It will print the commands that *would* be executed.
- `--force` or `-f`: Do not prompt for confirmation. Use with caution!
- `--help` or `-h`: Display help message.

### Examples:

1.  **Perform a full system prune (default behavior):**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-compost
    ```
    (Equivalent to `docker system prune -a -f` if `--force` is used, or `docker system prune -a` otherwise)

2.  **Prune only unused images, without confirmation:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-compost --images --force
    ```

3.  **See what would be pruned (dry run):**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-compost --all --dry-run
    ```

4.  **Prune specific components (e.g., containers and volumes):**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-compost --containers --volumes --force
    ```

## ⏰ Scheduling with Cron

For a truly `nightly` cleanup, you can schedule this utility using cron. Add a line like this to your crontab (`crontab -e`):

```cron
# Run the Docker Compost Bin every night at 3:00 AM
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-compost --all --force > /var/log/docker-compost.log 2>&1
```

Remember to replace `nightly-docker-compost` with the actual image name if you've tagged it differently or are using a specific registry path.

## ⚠️ Security Considerations

Mounting `/var/run/docker.sock` into a container grants that container root-level access to your Docker host. Only run trusted images and understand the implications. This utility is designed for system maintenance and should be used responsibly.
