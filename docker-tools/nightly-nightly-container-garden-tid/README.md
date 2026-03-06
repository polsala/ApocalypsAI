# Nightly Container Garden Tidy-Upper

## Overview

Welcome, digital gardener! Over time, your Docker environment can accumulate forgotten containers, orphaned images, and dangling volumes – much like weeds in a neglected garden. The `nightly-container-garden-tidy` utility is here to help you cultivate a clean and efficient Docker landscape.

This tool provides a whimsical yet powerful way to inspect and prune these digital weeds, freeing up precious disk space and ensuring your Docker ecosystem remains healthy and vibrant.

## Features

*   **Dry Run (Default)**: Safely inspects your Docker environment and reports what *could* be pruned without making any changes.
*   **Prune Mode**: Actively removes dangling images, stopped containers, unused networks, and dangling volumes.
*   **Containerized**: Runs as a Docker container itself, making it easy to deploy and use without installing additional dependencies on your host.

## Usage

To use the `nightly-container-garden-tidy`, you'll need Docker installed on your system. The utility needs access to your Docker daemon to perform its operations, which is achieved by mounting the Docker socket.

### 1. Build the Docker Image (Optional, or use pre-built if available)

First, navigate to the utility's directory and build its Docker image:

```bash
docker build -t nightly-container-garden-tidy .
```

### 2. Inspect Your Digital Garden (Dry Run)

To see what the utility *would* prune without actually making any changes, run it in dry-run mode (this is the default):

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-garden-tidy
```

Example Output (Dry Run):

```
🌿 Greetings, Digital Gardener! Time to inspect your container garden for any unruly digital weeds.

🔍 Found these potential weeds:

--- Dangling Images (forgotten seeds) ---
<none>

--- Exited Containers (withered blossoms) ---
<none>

--- Dangling Volumes (unclaimed soil plots) ---
<none>

--- Unused Networks (tangled roots) ---
<none>

🌱 Your garden looks remarkably tidy! No major pruning needed at this moment.

To perform actual pruning, run with the '--prune' flag.
```

### 3. Weed Your Digital Garden (Prune Mode)

To actually prune the identified items, run the utility with the `--prune` flag. **Use with caution, as this will remove items!**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-garden-tidy --prune
```

Example Output (Prune Mode):

```
✂️ Time to get pruning! Clearing out the digital weeds from your container garden.

Total reclaimed space: 123.4MB

✨ Your container garden is now sparkling clean! Happy cultivating!
```

## Development

### Running Tests

To run the automated tests, execute the `test_tidy_garden.sh` script. These tests use a mocked `docker` command to ensure determinism and offline execution.

```bash
bash tests/test_tidy_garden.sh
```
