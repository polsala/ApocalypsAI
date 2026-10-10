# Nightly Docker Mood Ring

Ever wonder how your containers are *feeling*? The `nightly-docker-mood-ring` is a whimsical, yet insightful, utility that assesses the 'mood' of your Docker containers based on their resource usage (CPU, memory) and health status.

It's a quick, at-a-glance way to check the operational state of your containers, perfect for local development or small-scale deployments where a visual cue is helpful.

## Moods Explained

The utility assigns one of the following moods:

*   **Serene 😌**: Healthy, low CPU (<20%) and memory (<20%) usage.
*   **Content 😊**: Healthy, moderate CPU (<50%) and memory (<50%) usage.
*   **Anxious 😟**: Healthy, but high CPU (>=50%) or memory (>=50%) usage.
*   **Grumpy 😠**: Unhealthy (Docker HEALTHCHECK failed).
*   **Furious 😡**: Container is restarting or has exited with a non-zero status.
*   **Asleep 😴**: Container is stopped or paused.
*   **Confused 🤔**: Container is running, but no detailed stats or health information is readily available.
*   **Vanished 👻**: Container not found.

## Usage

1.  **Build the Docker image:**

    ```bash
    docker build -t nightly-docker-mood-ring .
    ```

2.  **Run the utility:**

    You need to mount the Docker socket so the utility can communicate with the Docker daemon.

    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-mood-ring <container_name_or_id>
    ```

    Replace `<container_name_or_id>` with the actual name or ID of the container you want to check.

    **Example:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-mood-ring my-web-app
    ```

## Configuration (Environment Variables)

You can customize the thresholds for 'Anxious' mood by setting environment variables when running the container:

*   `CPU_ANXIOUS_THRESHOLD`: CPU usage percentage (default: `50`)
*   `MEM_ANXIOUS_THRESHOLD`: Memory usage percentage (default: `50`)

**Example with custom thresholds:**

```bash
docker run --rm \
  -e CPU_ANXIOUS_THRESHOLD=70 \
  -e MEM_ANXIOUS_THRESHOLD=80 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-docker-mood-ring my-resource-intensive-app
```

## Development

To run the Python script directly (for development/testing without Docker):

```bash
# Install dependencies
pip install -r requirements.txt

# Run the script (requires Docker daemon access)
python src/mood_ring.py <container_name_or_id>
```
