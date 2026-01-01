# Nightly Container Pet Sitter

## Summary

The `nightly-container-pet-sitter` is a whimsical-yet-useful Docker-based utility designed to keep an eye on your long-running, non-orchestrated Docker containers, affectionately dubbed 'pet containers'. It ensures they are running, reports their vital signs (CPU and Memory usage), and can even give them a 'snack' (restart) if they've unexpectedly stopped.

Think of it as a diligent digital pet sitter for your most cherished containers, ensuring they're always purring happily.

## How it Works

This utility runs as a Docker container itself. It connects to the Docker daemon (via a mounted socket) to inspect and manage other containers on the host. It iterates through a user-defined list of 'pet containers', checks their status, and performs actions based on configuration.

## Features

*   **Uptime Monitoring**: Checks if specified containers are running.
*   **Auto-Restart**: Optionally restarts containers that have exited.
*   **Resource Reporting**: Provides current CPU and Memory usage for active containers.
*   **Whimsical Logging**: Reports on your 'pets' status with a touch of charm.

## Configuration

The `nightly-container-pet-sitter` is configured via environment variables:

*   `PET_CONTAINERS` (required): A comma-separated list of Docker container names or IDs to monitor. Example: `my-db,my-app-server,monitoring-agent`.
*   `RESTART_ON_STOP` (optional): Set to `true` to automatically restart containers that have exited. Defaults to `false`. Example: `RESTART_ON_STOP=true`.
*   `CHECK_INTERVAL_SECONDS` (optional): How often (in seconds) the pet sitter should check on your containers. Defaults to `60`.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-container-pet-sitter` directory and build the image:

```bash
docker build -t container-pet-sitter .
```

### 2. Run the Pet Sitter

To run the pet sitter, you need to mount the Docker socket so it can communicate with the Docker daemon on your host. Configure your pet containers and restart preference using environment variables.

```bash
docker run -d \
  --name pet-sitter-agent \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e PET_CONTAINERS="my-precious-db,my-web-app" \
  -e RESTART_ON_STOP="true" \
  -e CHECK_INTERVAL_SECONDS="300" \
  container-pet-sitter
```

Replace `my-precious-db,my-web-app` with the actual names or IDs of your containers.

### 3. Check the Logs

Monitor the pet sitter's activity:

```bash
docker logs -f pet-sitter-agent
```

## Example Output

```
[2023-10-27 08:00:00] Nightly Container Pet Sitter is starting up...
[2023-10-27 08:00:00] Nightly Container Pet Sitter is making its rounds...
[2023-10-27 08:00:00] Checking on pet: my-precious-db
[2023-10-27 08:00:00] Pet 'my-precious-db' is happily purring. CPU: 0.50%, Mem: 128MiB / 1.952GiB
[2023-10-27 08:00:00] Checking on pet: my-web-app
[2023-10-27 08:00:00] Pet 'my-web-app' found sleeping.
[2023-10-27 08:00:00]   Attempting to wake up 'my-web-app'...
[2023-10-27 08:00:01]   Successfully woke up 'my-web-app'. It's now running.
[2023-10-27 08:00:01] Pet 'my-web-app' is happily purring. CPU: 1.20%, Mem: 256MiB / 3.906GiB
[2023-10-27 08:00:01] All pets checked. Will check again in 300 seconds.
```
