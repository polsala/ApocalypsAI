# ApocalypsAI Nightly Container Wrangler

A robust, yet whimsically named, utility designed to keep your Docker environment tidy by automatically stopping and removing ephemeral containers that have overstayed their welcome. No more zombie containers hogging resources!

## Purpose

In dynamic development or testing environments, it's common to spin up temporary Docker containers. Often, these "ephemeral" containers are forgotten, leading to resource bloat and clutter. The Nightly Container Wrangler acts as a digital shepherd, identifying containers marked for ephemerality and gracefully removing them once their expiration time has passed.

## How it Works

The Wrangler scans all Docker containers on the host. It looks for containers with specific labels:
- `apocalypsai.ephemeral=true`: Marks a container as an ephemeral candidate for wrangling.
- `apocalypsai.expires_at=<UNIX_TIMESTAMP>`: Specifies the Unix timestamp (seconds since epoch) when the container should be considered expired.

If a container is marked as ephemeral and its `expires_at` timestamp is in the past, the Wrangler will "wrangler" it by stopping and then removing it.

## Usage

This utility is designed to run as a Docker container itself, requiring access to the Docker daemon socket to manage other containers.

### 1. Build the Docker Image

Navigate to the `nightly-container-wrangler` directory and build the image:

```bash
docker build -t apocalypsai/container-wrangler .
```

### 2. Run the Wrangler

To run the Wrangler, you need to mount the Docker socket from your host into the container. This allows the Wrangler to interact with your host's Docker daemon.

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  apocalypsai/container-wrangler
```

**Explanation of parameters:**
- `--rm`: Automatically remove the container when it exits.
- `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon socket, giving the Wrangler control over other containers.

### 3. Scheduling (e.g., with Cron)

For continuous maintenance, you can schedule the Wrangler to run periodically using `cron` on your host system:

```cron
# Run the Container Wrangler every hour
0 * * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/container-wrangler >> /var/log/container-wrangler.log 2>&1
```

### 4. Marking Your Ephemeral Containers

When you create an ephemeral container, add the `apocalypsai.ephemeral=true` label and an `apocalypsai.expires_at` label with a future Unix timestamp.

**Example:**
```bash
# Create a temporary Nginx container that expires in 1 hour
EXPIRES_IN_1_HOUR=$(($(date +%s) + 3600))
docker run -d \
  --label apocalypsai.ephemeral=true \
  --label apocalypsai.expires_at="${EXPIRES_IN_1_HOUR}" \
  --name my-temp-nginx \
  nginx:latest
```

## Development and Testing

### Prerequisites

- Docker (for building the image)
- Bash (for running tests)

### Running Tests

The tests use a mocked `docker` command to simulate different container states without requiring a live Docker daemon.

```bash
bash tests/test_wrangler.sh
```

This will execute the test suite and report success or failure.

## Contributing

Feel free to suggest improvements or new features!
