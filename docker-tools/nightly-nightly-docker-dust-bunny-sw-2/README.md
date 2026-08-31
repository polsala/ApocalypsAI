# Nightly Docker Dust Bunny Sweeper

## Summary
The `nightly-docker-dust-bunny-sweeper` is a whimsical, yet highly practical, containerized utility designed to keep your Docker environment sparkling clean. It diligently sweeps away stale and unused Docker resources – including stopped containers, dangling images, unused volumes, and orphaned networks – preventing the accumulation of "digital dust bunnies" that can hog disk space and system resources.

## How it Works
This utility runs as a Docker container itself, connecting to the host's Docker daemon via the `/var/run/docker.sock`. It executes `docker prune` commands with configurable filters to target resources older than a specified number of days.

## Usage

### 1. Build the Docker Image
First, navigate to the `docker-tools/nightly-docker-dust-bunny-sweeper` directory and build the image:

```bash
docker build -t apocalypsai/dust-bunny-sweeper .
```

### 2. Run the Sweeper

To run the sweeper, you need to mount the Docker socket from your host into the container. This allows the container to interact with your host's Docker daemon.

**Basic Cleanup (default: prune resources older than 7 days):**
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper
```

**Custom Age Cleanup (e.g., prune resources older than 30 days):**
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --days-old 30
```

**Dry Run (see what would be cleaned without actually doing it):**
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --dry-run
```

**Verbose Output:**
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --verbose
```

**Combined Options:**
```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/dust-bunny-sweeper --days-old 14 --dry-run --verbose
```

### Options:
*   `--days-old N`: Prune resources older than `N` days (default: `7`).
*   `--dry-run`: Show what would be cleaned without actually performing the deletion.
*   `--verbose`: Enable verbose logging to see the sweeper's progress and whimsical messages.
*   `-h`, `--help`: Display usage information.

## Automated Tests
The tests for this utility are located in `tests/test_cleanup.sh`. They use a mocked `docker` command to verify that the `cleanup.sh` script correctly constructs and attempts to execute the expected `docker prune` commands with the specified filters, without requiring an actual Docker daemon to be running or modifying the system.

To run the tests:
```bash
bash tests/test_cleanup.sh
```
