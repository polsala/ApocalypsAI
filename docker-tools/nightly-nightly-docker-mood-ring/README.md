# nightly-docker-mood-ring

A whimsical containerized utility that monitors the state of your Docker containers and translates their operational status into relatable "moods." Ever wondered if your database is feeling "Grumpy" or your web server is "Joyful"? Now you'll know!

## Summary

The `nightly-docker-mood-ring` is a Docker container that connects to your Docker daemon, periodically lists active containers, and assigns a "mood" based on their current status and health checks. It prints these moods to standard output, providing a lighthearted glance into your container ecosystem's emotional state.

## How it Works

1.  **Containerized Execution**: The utility runs as its own Docker container.
2.  **Docker Daemon Access**: It requires access to the Docker daemon socket (`/var/run/docker.sock`) to inspect other containers.
3.  **Periodic Monitoring**: Every few seconds (configurable), it queries the Docker daemon for a list of containers.
4.  **Mood Assignment**: Based on the container's `status` (e.g., `running`, `exited`, `restarting`) and `health status` (if available), it assigns a whimsical mood.
5.  **Output**: The container's name, short ID, and its current mood are printed to `stdout`.

## Moods Explained

Here's how the `nightly-docker-mood-ring` interprets your containers' feelings:

*   **Joyful**: Container is `running` and its health check reports `healthy`. All is well in the container-verse!
*   **Content**: Container is `running`, but either has no health check or its health status is unknown. It's doing its job, quietly.
*   **Grumpy**: Container is `running`, but its health check reports `unhealthy`. Something's not quite right, it might need a hug (or a restart).
*   **Sleepy**: Container is `exited`. It's taking a well-deserved nap.
*   **Anxious**: Container is `restarting`. It's a bit flustered and trying to get back on its feet.
*   **Pensive**: Container is `paused`. Deep in thought, or just taking a break.
*   **At Peace (Exited Permanently)**: Container is `dead`. It has gracefully (or not so gracefully) departed.
*   **Mysterious**: Any other or unknown status. Who knows what secrets it holds?

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-docker-mood-ring` directory and build the image:

```bash
docker build -t apocalypsai/docker-mood-ring .
```

### 2. Run the Container

You need to mount the Docker socket so the `mood-ring` can see other containers.

```bash
docker run -d \
  --name docker-mood-ring-instance \
  -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/docker-mood-ring
```

### 3. View the Moods

Check the logs of the `docker-mood-ring-instance` container:

```bash
docker logs -f docker-mood-ring-instance
```

### Configuration (Environment Variables)

You can customize the monitoring behavior using environment variables:

*   `DOCKER_MOOD_RING_INTERVAL`: The interval (in seconds) between monitoring checks. Defaults to `5`.
    Example: `docker run -e DOCKER_MOOD_RING_INTERVAL=10 ...`
*   `DOCKER_MOOD_RING_TARGETS`: A comma-separated list of container names to monitor. If not set, all containers are monitored.
    Example: `docker run -e DOCKER_MOOD_RING_TARGETS="my-web-app,my-database" ...`

### Example Output

```
ApocalypsAI Docker Mood Ring activated!
Monitoring containers every 5 seconds. Press Ctrl+C to stop.
[2023-10-27 10:30:01] Container 'my-web-app' (ID: a1b2c3d4): Joyful
[2023-10-27 10:30:01] Container 'my-database' (ID: e5f6g7h8): Content
[2023-10-27 10:30:01] Container 'unhealthy-service' (ID: i9j0k1l2): Grumpy
[2023-10-27 10:30:06] Container 'my-web-app' (ID: a1b2c3d4): Joyful
[2023-10-27 10:30:06] Container 'my-database' (ID: e5f6g7h8): Content
[2023-10-27 10:30:06] Container 'unhealthy-service' (ID: i9j0k1l2): Grumpy
```
