# Nightly Container Compost Heap

## 🌿 Overview

The `nightly-container-compost` is a whimsical yet practical Docker-based utility designed to help you keep your Docker environment tidy. It scans for unused Docker images, volumes, and networks – the "digital dust bunnies" and "forgotten container remnants" – and helps you turn them into fertile "digital compost" to free up valuable disk space. Think of it as a friendly gardener for your container ecosystem!

## ✨ Features

*   **Dry Run Mode (Default):** Get a "Digital Compost Report" detailing what *would* be pruned without making any actual changes.
*   **Prune Mode:** Actively remove unused Docker resources, reclaiming disk space.
*   **Containerized:** Runs as a self-contained Docker image, ensuring consistent behavior across environments.

## 🚀 How to Use

### Prerequisites

*   Docker installed and running on your host machine.
*   The container needs access to the Docker daemon socket to interact with your host's Docker environment.

### 1. Build the Docker Image

Navigate to the `nightly-container-compost` directory and build the image:

```bash
docker build -t nightly-container-compost .
```

### 2. Run in Dry Run Mode (Recommended First)

To see what resources are ripe for composting without actually removing them:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-compost --dry-run
```

This will output a "Digital Compost Report" to your console.

### 3. Run in Prune Mode

**Use with caution!** This command will permanently remove unused Docker images, volumes, and networks (specifically, those not associated with any running container and older than 24 hours).

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-compost --prune
```

You will see a confirmation message if the composting process is successful.

### 4. Schedule with Cron (Example)

For regular tidying, you can schedule this utility using a cron job on your host system.

**Example Cron Entry (runs every Sunday at 3 AM in dry-run mode):**

```cron
0 3 * * SUN docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-compost --dry-run >> /var/log/docker-compost-report.log 2>&1
```

**Example Cron Entry (runs every Sunday at 4 AM in prune mode - use with extreme care!):**

```cron
0 4 * * SUN docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-container-compost --prune >> /var/log/docker-compost-action.log 2>&1
```

Always review the dry-run report before enabling automated pruning.

## 🧪 Testing

To run the automated tests for the `compost_heap.sh` script:

```bash
bash tests/test_compost_heap.sh
```

These tests use a mocked `docker` command to ensure no actual system changes occur during testing.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
