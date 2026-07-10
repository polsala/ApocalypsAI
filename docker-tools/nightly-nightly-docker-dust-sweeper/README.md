# Nightly Docker Dust Sweeper

🧹✨ **A Whimsical Containerized Cleanup Crew for Your Docker-verse!** ✨🧹

Are your Docker environments feeling a bit cluttered? Are digital dust bunnies accumulating in the forgotten corners of your container registry? Fear not! The `Nightly Docker Dust Sweeper` is here to magically whisk away unused images, stopped containers, dangling volumes, and orphaned networks, leaving your Docker-verse sparkling clean and efficient.

This utility is designed to run as a Docker container itself, connecting to your host's Docker daemon to perform its tidying tasks.

## Features

*   **Comprehensive Cleanup:** Targets unused images, stopped containers, dangling volumes, and orphaned networks.
*   **Whimsical Reporting:** Provides delightful messages as it cleans, making cleanup a joy.
*   **Dry Run Mode:** Safely preview what *would* be swept away before committing to the cleanup.
*   **Containerized:** Runs in its own isolated Docker container, requiring only Docker to be installed on your host.

## Usage

### 1. Build the Docker Image

First, you need to build the `nightly-docker-dust-sweeper` image. Navigate to the utility's directory and run:

```bash
docker build -t nightly-docker-dust-sweeper .
```

### 2. Run the Sweeper

To run the sweeper, you need to mount your host's Docker socket (`/var/run/docker.sock`) into the container. This allows the sweeper to interact with your Docker daemon.

#### Dry Run (Recommended First!)

Always start with a dry run to see what will be cleaned without actually deleting anything:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-dust-sweeper --dry-run
```

This command will output a report of all the digital dust bunnies it *would* sweep away.

#### Actual Cleanup

Once you're confident with the dry run report, you can proceed with the actual cleanup:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-dust-sweeper
```

This command will execute `docker system prune -f --volumes` on your host, removing:

*   All stopped containers
*   All dangling images
*   All unused networks
*   All dangling build cache
*   All unused volumes (if `--volumes` is used, which it is by default in this script)

**⚠️ Caution:** Running this command will permanently remove resources. Ensure you understand its implications or use the `--dry-run` option first.

## How it Works

The `sweep.sh` script inside the container simply executes `docker system prune -f --volumes` (or performs a detailed listing for `--dry-run`) against the Docker daemon accessible via the mounted socket. It then parses the output to provide a friendly summary.

## Development & Testing

To test the `sweep.sh` script locally without building the Docker image or affecting your actual Docker environment, you can use the provided `tests/test_sweep.sh` script. This script uses a mock `docker` command to simulate interactions.

```bash
./tests/test_sweep.sh
```

This will run the tests and ensure the script behaves as expected under various conditions.
