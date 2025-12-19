# Nightly Docker Dust Bunny Sweeper 🧹✨

A whimsical Docker utility to sweep away digital dust bunnies (stale images, volumes, and networks) and reclaim precious disk space. Keep your Docker environment sparkling clean and efficient!

## 🌟 Features

*   **Comprehensive Pruning**: Targets unused images, volumes, networks, and build cache.
*   **Granular Control**: Choose to prune specific types of Docker objects or sweep everything at once.
*   **Dry Run Mode**: See what would be swept away before committing to the cleanup.
*   **Force Mode**: Bypass confirmation prompts for automated cleanups.
*   **Containerized**: Runs as a Docker container, ensuring consistent behavior across environments.

## 🚀 How to Use

This utility is designed to be run as a Docker container, interacting with your host's Docker daemon.

### 1. Build the Docker Image (Optional, if not using a pre-built image)

First, navigate to the utility's directory and build the Docker image:

```bash
docker build -t apocalypsai/dust-bunny-sweeper .
```

### 2. Run the Sweeper

To run the sweeper, you need to mount the Docker socket from your host into the container. This allows the containerized script to execute `docker` commands against your host's Docker daemon.

**Important**: Running containers with access to the Docker socket (`/var/run/docker.sock`) grants them root-level access to your Docker host. Use with caution and only with trusted images.

#### Basic Cleanup (Prune all unused objects, with confirmation)

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper
```
This will prompt you for confirmation before pruning.

#### Force Cleanup (Prune all unused objects, no confirmation)

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --force
```

#### Dry Run (See what would be pruned without actually doing it)

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --dry-run
```

#### Prune Specific Types (e.g., only images and volumes)

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --images --volumes --force
```

#### View Help

```bash
docker run --rm apocalypsai/dust-bunny-sweeper --help
```

### 🧹 Available Options

The `dust_bunny_sweeper.sh` script supports the following command-line arguments:

*   `-a`, `--all`: Prune all unused Docker objects (images, containers, networks, volumes, build cache). This is the default if no specific type is provided.
*   `-i`, `--images`: Prune unused images (dangling images).
*   `-v`, `--volumes`: Prune unused volumes.
*   `-n`, `--networks`: Prune unused networks.
*   `-b`, `--build-cache`: Prune the build cache.
*   `-d`, `--dry-run`: Show what would be pruned without actually doing it.
*   `-f`, `--force`: Do not prompt for confirmation.
*   `-h`, `--help`: Display the help message.

## 🧪 Development & Testing

To run the tests, you'll need `bash`.

```bash
# Navigate to the utility's directory
cd nightly-docker-dust-bunny-sweeper

# Run the tests
bash tests/test_sweeper.sh
```

The tests use a mock `docker` function to prevent actual interaction with your Docker daemon, ensuring they are deterministic and offline.
