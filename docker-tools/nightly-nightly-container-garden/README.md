# Nightly Container Garden Tidy-Upper

Ever feel like your Docker environment is an overgrown jungle? The `Nightly Container Garden Tidy-Upper` is here to help! This whimsical Docker-based utility scans your system for forgotten images, withered containers, and empty volumes, presenting them as a delightful garden report. It then suggests "pruning" commands to keep your digital ecosystem neat and efficient.

## Features

*   **Garden Scan**: Identifies dangling images, exited containers, and unused volumes.
*   **Whimsical Report**: Presents findings with charming garden metaphors.
*   **Pruning Suggestions**: Provides `docker` commands to clean up identified clutter.
*   **Dry Run Mode**: See what would be pruned without making any changes.

## Usage

First, build the Docker image:

```bash
docker build -t nightly-container-garden .
```

Then, run the utility. It needs access to the Docker daemon, so mount the Docker socket:

### Dry Run (Recommended First)

To get your garden report without making any changes:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-garden
```

### Prune Your Garden

To actually clean up the identified resources (use with caution!):

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-garden --prune
```

### Specific Cleanup (Advanced)

The report will also suggest specific `docker rmi`, `docker rm`, `docker volume rm` commands for more granular control.

## How it Works

The utility runs a Python script inside a minimal Docker container. This script interacts with your host's Docker daemon (via the mounted `/var/run/docker.sock`) to query resource usage and status. It then parses the output and formats it into a human-readable, garden-themed report.

## Development

To run the Python script directly (for development or if Docker is not available, but you have `docker` CLI installed and accessible):

```bash
python3 src/main.py
```

Or with pruning:

```bash
python3 src/main.py --prune
```

## Tests

Tests are located in `tests/test_main.py`. To run them:

```bash
python3 -m pytest tests/test_main.py
```
