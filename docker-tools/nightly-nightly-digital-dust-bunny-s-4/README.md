# Nightly Digital Dust Bunny Sweeper (Fluffernutter)

## Summary
A containerized digital dust bunny that periodically cleans up unused Docker resources, reporting its 'satisfaction' level.

## Description
Fluffernutter is a diligent, albeit fluffy, guardian of your Docker environment. It scurries through your system, identifying and "eating" orphaned images, stopped containers, dangling volumes, and unused networks. The more digital dust it consumes, the happier (and more satisfied) Fluffernutter becomes! By regularly running Fluffernutter, you can keep your Docker daemon tidy, reclaim disk space, and prevent resource clutter.

## Features
*   **Automated Cleanup**: Periodically prunes unused Docker images, containers, volumes, and networks.
*   **Whimsical Reporting**: Fluffernutter reports its "satisfaction level" based on the amount of digital dust consumed.
*   **Dry Run Mode**: Test what would be cleaned without actually removing any resources.
*   **Configurable Interval**: Set how often Fluffernutter performs its sweep.

## Usage

### Prerequisites
*   Docker installed and running on your host machine.

### 1. Build the Docker Image
Navigate to the `nightly-digital-dust-bunny-sweeper` directory and build the image:

```bash
docker build -t fluffernutter .
```

### 2. Run Fluffernutter
To run Fluffernutter, you need to mount the Docker socket so it can communicate with your Docker daemon. It's recommended to run it as a detached container.

```bash
docker run -d \
  --name fluffernutter \
  -v /var/run/docker.sock:/var/run/docker.sock \
  fluffernutter
```

Fluffernutter will start sweeping immediately and then every hour by default.

### Configuration (Environment Variables)
You can customize Fluffernutter's behavior using environment variables:

*   `CLEANUP_INTERVAL_SECONDS`: The interval (in seconds) between cleanup sweeps. Default is `3600` (1 hour).
    *   Example: `docker run ... -e CLEANUP_INTERVAL_SECONDS=600 ... fluffernutter` (sweep every 10 minutes)
*   `DRY_RUN`: Set to `true` to enable dry-run mode. Fluffernutter will report what it *would* clean without actually removing anything. Default is `false`.
    *   Example: `docker run ... -e DRY_RUN=true ... fluffernutter`

### Example Run with Dry Run
```bash
docker run --rm \
  --name fluffernutter-dry-run \
  -e DRY_RUN=true \
  -e CLEANUP_INTERVAL_SECONDS=10 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  fluffernutter
```
This will run Fluffernutter in dry-run mode, sweeping every 10 seconds (for demonstration), and remove the container after it exits (which it won't, as it's a continuous service, but `--rm` is good practice for one-off tests).

### Stopping Fluffernutter
```bash
docker stop fluffernutter
docker rm fluffernutter
```

## Fluffernutter's Output
Fluffernutter logs its activities and mood to standard output. You can view its logs:

```bash
docker logs -f fluffernutter
```

Example log output:
```
2023-10-27 08:00:00,123 - INFO - Fluffernutter, the Digital Dust Bunny Sweeper, is starting up!
2023-10-27 08:00:00,123 - INFO - Cleanup interval: 3600 seconds. Dry run: false
2023-10-27 08:00:00,123 - INFO - --- Fluffernutter is beginning its sweep! ---
2023-10-27 08:00:00,124 - INFO - Fluffernutter is sniffing out unused images...
2023-10-27 08:00:00,500 - INFO - Fluffernutter munched 5 unused images!
2023-10-27 08:00:00,501 - INFO - Fluffernutter is tidying up stopped containers...
2023-10-27 08:00:00,700 - INFO - Fluffernutter tucked away 2 stopped containers!
2023-10-27 08:00:00,701 - INFO - Fluffernutter is sweeping up dangling volumes...
2023-10-27 08:00:00,900 - INFO - No dangling volumes for Fluffernutter to roll around in.
2023-10-27 08:00:00,901 - INFO - Fluffernutter is untangling unused networks...
2023-10-27 08:00:01,100 - INFO - Fluffernutter untangled 1 unused network!
2023-10-27 08:00:01,101 - INFO - --- Fluffernutter's Report ---
2023-10-27 08:00:01,101 - INFO - Images pruned: 5
2023-10-27 08:00:01,101 - INFO - Containers pruned: 2
2023-10-27 08:00:01,101 - INFO - Volumes pruned: 0
2023-10-27 08:00:01,101 - INFO - Networks pruned: 1
2023-10-27 08:00:01,101 - INFO - Fluffernutter's current mood: Ecstatic! (a veritable feast of digital dust!)
2023-10-27 08:00:01,101 - INFO - --- Sweep complete. Fluffernutter will rest for 3600 seconds. ---
```

## Development

### Running Tests
Tests are self-contained within a Docker container to ensure a consistent environment and mock Docker interactions.

```bash
docker build -f tests/Dockerfile.test -t fluffernutter-tests .
docker run --rm fluffernutter-tests
```
