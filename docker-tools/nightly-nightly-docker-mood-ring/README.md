# Nightly Docker Mood Ring

A whimsical-yet-useful containerized utility that monitors the state of your Docker containers and expresses their "mood" based on their operational status and health checks. Ever wondered if your database container is feeling "Serene" or if your web server is a bit "Anxious"? This tool has you covered!

## Features

*   **Mood-based Status:** Translates technical Docker container states into relatable "moods."
*   **Health Check Integration:** Considers Docker's built-in health checks for more nuanced moods.
*   **Easy to Deploy:** Runs as a self-contained Docker container.
*   **Configurable:** Specify which containers to monitor via an environment variable.

## Moods Explained

*   **Serene 😌:** The container is `running` and its Docker health check (if defined) reports `healthy`. All is well in its little container world.
*   **Anxious 😨:** The container is `running` but its health check reports `unhealthy` or `starting`, or the container is in a `restarting` state. It might be feeling a bit stressed.
*   **Grumpy 😠:** The container is `exited` or `stopped`. It's not happy and probably needs a restart.
*   **Pensive 🧠:** The container is `running`, but it doesn't have a Docker health check defined, or its health status is unknown. It's just doing its thing, quietly contemplating.
*   **Invisible 👻 (Not Found):** The specified container name or ID could not be found by the Docker daemon. It might have vanished!
*   **Troubled ⛈️ (API Error):** An error occurred while communicating with the Docker daemon. Something's amiss in the Docker infrastructure itself.
*   **Confused 😵 (Error):** An unexpected error occurred within the Mood Ring utility.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-docker-mood-ring` directory and build the image:

```bash
docker build -t docker-mood-ring .
```

### 2. Run the Mood Ring

To use the Mood Ring, you need to run it as a Docker container and mount the Docker socket (`/var/run/docker.sock`) from your host. This allows the Mood Ring container to communicate with your host's Docker daemon and inspect other containers.

You must also provide a comma-separated list of container names or IDs you wish to monitor via the `CONTAINER_NAMES` environment variable.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e "CONTAINER_NAMES=my-web-app,my-database,another-service-id" \
  docker-mood-ring
```

Replace `my-web-app,my-database,another-service-id` with the actual names or IDs of the containers you want to check.

#### Example Output:

```
--- Docker Mood Ring Report (2023-10-27 10:30:00) ---
Container 'my-web-app': Serene 😌
Container 'my-database': Anxious 😨
Container 'non-existent-app': Invisible 👻 (Not Found)
Container 'my-stopped-app': Grumpy 😠
--------------------------------------------------
```

### 3. Integrate into Automation (Optional)

You can integrate this utility into your CI/CD pipelines, monitoring scripts, or cron jobs to get regular updates on your container's emotional well-being.

```bash
# Example cron job (runs every 5 minutes)
# */5 * * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e "CONTAINER_NAMES=my-app,my-db" docker-mood-ring >> /var/log/docker-mood-ring.log 2>&1
```

## Development

### Prerequisites

*   Docker
*   Python 3.9+
*   `pip`

### Setup

```bash
# Install dependencies
pip install -r src/requirements.txt
```

### Running Locally (for development/testing)

You can run the Python script directly if you have the `docker` Python library installed and access to the Docker daemon.

```bash
export CONTAINER_NAMES="my-web-app,my-database" # Replace with actual container names
python src/mood_ring.py
```

### Running Tests

```bash
python -m unittest tests/test_mood_ring.py
```
