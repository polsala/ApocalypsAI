# Nightly Docker Mood Ring 💍

Ever wondered if your Docker containers are feeling "Zen" or "Overwhelmed"? The Nightly Docker Mood Ring is a whimsical-yet-useful utility that assigns a "mood" to each of your running Docker containers based on their real-time resource usage (CPU, Memory) and status. Get an at-a-glance emotional readout of your container ecosystem!

## Features

*   **Whimsical Moods**: Containers are assigned moods like "Zen 🙏", "Overwhelmed 🥵", "Snoozing 😴", and more.
*   **Resource-Based Insights**: Moods are derived from CPU and Memory utilization, giving you a quick indicator of performance.
*   **Status Awareness**: Identifies containers that are "Lost in the Void 👻" (not running).
*   **Easy to Use**: Runs as a Docker container itself, connecting to your host's Docker daemon.

## Mood Definitions

*   **Lost in the Void 👻**: Container is not running (exited, dead, created, etc.).
*   **Overwhelmed 🥵**: High CPU (>85%) or Memory (>85%) usage.
*   **Anxious 😬**: Moderate CPU (>50%) or Memory (>50%) usage.
*   **Busy Bee 🐝**: Active CPU (>10%) or Memory (>10%) usage, but not stressed.
*   **Zen 🙏**: Normal, healthy operation (CPU/Mem between 5% and 10%).
*   **Snoozing 😴**: Very low CPU (<5%) and Memory (<5%) usage.

## Usage

To run the Docker Mood Ring, you need to have Docker installed and running on your system. The utility runs as a Docker container and requires access to the Docker daemon socket (`/var/run/docker.sock`) to inspect other containers.

1.  **Build the Docker image:**
    ```bash
    docker build -t nightly-docker-mood-ring .
    ```

2.  **Run the utility container:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-mood-ring
    ```
    *   `--rm`: Automatically remove the container when it exits.
    *   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon socket from your host into the utility container, allowing it to communicate with the Docker daemon.

### Example Output

```
--- Docker Container Mood Ring ---
Scan Time: 2023-10-27 10:30:00

Container Name                 ID (short)      Status          CPU %      Mem %      Mood
------------------------------ --------------- --------------- ---------- ---------- --------------------
my-web-app                     a1b2c3d4e5f6    running         40.50%     65.20%     Anxious 😬
database-server                f7e6d5c4b3a2    running         12.10%     30.80%     Busy Bee 🐝
monitoring-agent               1a2b3c4d5e6f    running         5.00%      7.50%      Zen 🙏
idle-service                   9z8y7x6w5v4u    running         0.10%      1.20%      Snoozing 😴
old-test-container             p0o9i8u7y6t5    exited          0.00%      0.00%      Lost in the Void 👻
```

## Development

### Prerequisites

*   Python 3.9+
*   Docker
*   `docker` Python package (`pip install docker`)

### Running Tests

To run the unit tests for the mood assignment logic (without needing a Docker daemon):

```bash
python -m unittest tests/test_app.py
```

### Local Execution (without Docker container)

You can also run the Python script directly, provided you have the `docker` Python SDK installed and access to the Docker daemon (e.g., via `DOCKER_HOST` environment variable or default socket).

```bash
pip install docker
python src/app.py
```

## Contributing

Feel free to suggest new moods, refine the mood logic, or add more metrics!
