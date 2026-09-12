# Nightly Container Compost Collector

## Summary

The `nightly-container-compost-collector` is a whimsical yet highly practical Docker utility designed to keep your development and production environments tidy. It identifies and prunes stale Docker containers, dangling images, and unused volumes, metaphorically turning digital clutter into fertile ground for new projects. Think of it as a digital gardener for your Docker ecosystem, ensuring only the freshest flora thrives.

## How it Works

This utility runs inside a Docker container and interacts with your host's Docker daemon (via `/var/run/docker.sock`). It performs a scan to identify resources that are no longer actively used or are in an 'exited' state for a prolonged period. By default, it operates in a 'dry-run' mode, reporting what *would* be composted. With the `--force` flag, it proceeds with the actual pruning using `docker system prune --all --force --volumes`, which is a comprehensive cleanup command.

## Usage

### 1. Build the Docker Image

First, you need to build the `compost-collector` Docker image:

```bash
docker build -t compost-collector .
```

### 2. Run the Collector

To run the utility, you need to mount your Docker socket so the container can interact with the Docker daemon.

#### Dry Run (Recommended First Step)

This will show you what resources would be composted without actually removing anything:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock compost-collector --dry-run
```

Example Output (Dry Run):
```
🌿 Nightly Container Compost Collector Initiated 🌿

Scanning for digital detritus...

Found 1 exited container(s) ready for composting:
  - Container ID: c1234567890a, Name: stale_app_container

Found 1 dangling image(s) for decomposition:
  - Image ID: i1234567890a, Repository: <none>, Tag: <none>

Found 1 unused volume(s) to return to the earth:
  - Volume Name: old_data_volume

This was a dry run. No resources were composted. To proceed, run with '--force'.
🌱 Your digital garden awaits its refresh! 🌱
```

#### Force Run (Actual Composting)

**Use with caution!** This will permanently remove identified stale resources.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock compost-collector --force
```

Example Output (Force Run):
```
🌿 Nightly Container Compost Collector Initiated 🌿

Scanning for digital detritus...

Found 1 exited container(s) ready for composting:
  - Container ID: c1234567890a, Name: stale_app_container

Found 1 dangling image(s) for decomposition:
  - Image ID: i1234567890a, Repository: <none>, Tag: <none>

Found 1 unused volume(s) to return to the earth:
  - Volume Name: old_data_volume

Initiating digital decomposition...

Total reclaimed space: 100MB

Composting complete! Your digital garden is refreshed.
✨ Enjoy the clean, fertile ground for new growth! ✨
```

#### Default Behavior (Dry Run)

If no arguments are provided, the utility defaults to a dry run:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock compost-collector
```

This will produce the same output as `docker run ... --dry-run`.
