# Nightly Container Mood Ring

## Overview

The `nightly-container-mood-ring` is a whimsical yet practical utility designed to give you a quick, intuitive glance at the "emotional state" of your Docker containers. Instead of sifting through raw logs or complex metrics, this tool assigns a "mood" to your containers based on their resource usage, log activity, and status. It's perfect for local development environments or small-scale deployments where you need a fast, human-readable summary of your container's well-being.

## Features

*   **Whimsical Moods:** Containers are assigned moods like "Jubilant", "Anxious", "Grumpy", or "Serene".
*   **Resource Monitoring:** Checks CPU and memory usage.
*   **Log Analysis:** Scans recent logs for warnings and errors.
*   **Status Awareness:** Differentiates between running, stopped, and frequently restarting containers.
*   **Containerized:** Runs as its own Docker container, easily integrating into your existing Docker setup.

## Mood Definitions

*   **Jubilant:** Running, low resource usage, no errors, recent activity. All good!
*   **Serene:** Running, normal resource usage, no errors. Calm and collected.
*   **Bored:** Running, very low resource usage, no errors, no recent activity. Waiting for something to do.
*   **Anxious:** Running, high CPU or memory usage. Feeling the pressure.
*   **Grumpy:** Running, moderate resource usage, warnings in logs. A bit irritable.
*   **Distressed:** Running, critical resource usage, errors in logs. Needs immediate attention!
*   **Fickle:** Running, but has restarted recently. Unstable, prone to mood swings.
*   **Asleep:** Stopped/Exited gracefully. Resting.
*   **Deceased:** Exited with a non-zero code. Something went wrong.
*   **Invisible:** Container not found. Where did it go?

## Usage

### 1. Build the Mood Ring Image

Navigate to the `nightly-container-mood-ring` directory and build the Docker image:

```bash
docker build -t container-mood-ring .
```

### 2. Run the Mood Ring

You can run the `container-mood-ring` against any running Docker container. It needs access to the Docker daemon, so you'll typically mount the Docker socket.

**Example with `docker run`:**

To check the mood of a container named `my-app-container`:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock container-mood-ring my-app-container
```

**Example with `docker-compose` (recommended for multi-container setups):**

1.  Ensure you have a `docker-compose.yml` file in your project (see `docker-compose.yml` in this directory for an example).
2.  Start your target containers (e.g., `my-app-container`):
    ```bash
    docker-compose up -d my-app-container
    ```
3.  Run the mood ring against your target container(s):
    ```bash
    docker-compose run --rm mood-ring my-app-container
    # Or for multiple containers:
    # docker-compose run --rm mood-ring my-app-container database-service
    ```

### 3. Interpreting the Output

The utility will output a line for each monitored container, indicating its name, mood, and a brief reason.

```
Container my-app-container: Serene - Normal operation, no issues.
Container database-service: Anxious - High CPU usage detected (85%).
Container old-service: Deceased - Exited with status 1.
```

## Development

### Running Tests

To run the Python unit tests for the mood determination logic (without needing a Docker daemon):

```bash
pip install -r src/requirements.txt
python -m pytest tests/test_mood_ring.py
```
