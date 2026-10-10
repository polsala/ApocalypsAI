# Nightly Temporal Docker Janitor

## 🌌 Overview

The `nightly-temporal-docker-janitor` is a whimsical-yet-useful utility designed to help you maintain a clean Docker environment. It acts as a 'temporal janitor,' sweeping through your Docker daemon to identify and remove exited containers older than a specified number of days, and to clear out any 'dangling' images (those not tagged or referenced by any container).

This tool helps reclaim disk space and keeps your Docker timelines tidy, preventing clutter from forgotten experiments and past computations.

## ✨ Features

-   **Container Cleanup**: Removes exited containers that have been lingering for too long.
-   **Dangling Image Pruning**: Deletes untagged images that are no longer referenced, freeing up valuable disk space.
-   **Whimsical Messaging**: Provides delightful, time-travel-themed messages during the cleanup process.
-   **Dry Run Mode**: Safely preview what would be removed without making any actual changes.
-   **Configurable Age**: Specify how many days old an exited container must be to be considered for removal.

## 🚀 Usage

To use the Temporal Docker Janitor, you'll first need to build its Docker image, then run it with access to your Docker daemon.

### 1. Build the Janitor Image

Navigate to the utility's directory and build the Docker image:

```bash
docker build -t temporal-docker-janitor .
```

### 2. Run the Janitor

To allow the janitor to interact with your host's Docker daemon, you must mount the Docker socket (`/var/run/docker.sock`) into the container. 

**Basic Cleanup (removes exited containers older than 7 days and all dangling images):**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-docker-janitor
```

**Dry Run (see what would be removed without actually removing anything):**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-docker-janitor --dry-run
```

**Specify a different age for containers (e.g., remove containers older than 30 days):**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-docker-janitor --days-old 30
```

**Force removal (useful for stubborn resources):**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-docker-janitor --force
```

**Combine options:**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock temporal-docker-janitor --dry-run --days-old 14
```

## 🧪 Testing

The tests for the `nightly-temporal-docker-janitor` are self-contained and use a mocked `docker` command to ensure determinism and offline execution.

To run the tests, execute the `test_janitor.sh` script:

```bash
bash tests/test_janitor.sh
```

This script will set up a temporary mock `docker` executable in your PATH, run the `temporal_janitor.sh` script with various arguments, and assert its output. It also overrides the current date for consistent temporal comparisons.
