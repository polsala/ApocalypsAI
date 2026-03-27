# Nightly Docker Mood Lamp

## 💡 Whimsical-yet-Useful Docker Stack Health Monitor 💡

The `nightly-docker-mood-lamp` is a delightful little utility that brings a touch of color and whimsy to your terminal, while providing a quick, at-a-glance overview of your Docker Compose stack's health.

Instead of digging through `docker ps` or `docker-compose ps`, let the Mood Lamp tell you if your services are humming along happily, feeling a bit under the weather, or have completely thrown a tantrum.

## ✨ Features

- **Visual Health Indicators:** Outputs colored emojis and messages to your terminal based on your Docker Compose stack's health.
- **Containerized:** Runs as a standalone Docker container, requiring only access to the Docker daemon.
- **Configurable:** Specify the Docker Compose project name to monitor.
- **Periodic Checks:** Continuously monitors your stack at a configurable interval.

## 🌈 Moods

- 🟢 **Green (All Systems Go!):** All services in the stack are running and healthy.
- 🟡 **Yellow (A Bit Wobbly...):** Some services are restarting, paused, or have health checks indicating degradation.
- 🔴 **Red (Uh Oh, Trouble in Paradise!):** One or more services have exited, are unhealthy, or failed to start.
- 🔵 **Blue (Just Waking Up...):** Initializing, or no containers found for the specified project yet.

## 🚀 Usage

To run the Docker Mood Lamp, you need to mount the Docker socket so it can communicate with your Docker daemon. You also need to specify the `COMPOSE_PROJECT_NAME` environment variable, which corresponds to the name of your Docker Compose project (usually the directory name where your `docker-compose.yml` resides, or explicitly set via `COMPOSE_PROJECT_NAME`).

```bash
# Example: Monitoring a project named 'myproject'
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e COMPOSE_PROJECT_NAME=myproject \
  nightly-docker-mood-lamp
```

### Configuration Options

- `COMPOSE_PROJECT_NAME` (required): The name of the Docker Compose project to monitor.
- `CHECK_INTERVAL_SECONDS` (optional, default: `5`): How often (in seconds) to check the stack's health.

```bash
# Example with custom interval
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -e COMPOSE_PROJECT_NAME=myproject \
  -e CHECK_INTERVAL_SECONDS=10 \
  nightly-docker-mood-lamp
```

## 🛠️ Development

### Building the Docker Image

```bash
docker build -t nightly-docker-mood-lamp .
```

### Running Tests

Tests are self-contained and do not require a running Docker daemon. They mock the Docker SDK interactions.

```bash
python3 -m unittest tests/test_app.py
```

## ⚠️ Important Notes

- **Docker Socket Access:** This utility requires read-only access to `/var/run/docker.sock`. Ensure you understand the security implications of mounting the Docker socket.
- **Health Checks:** For accurate 'healthy'/'unhealthy' statuses, ensure your services in `docker-compose.yml` define `healthcheck` configurations.
