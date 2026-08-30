# Nightly Container Compost Heap

## Summary

The `nightly-container-compost` is a whimsical-yet-essential Docker utility designed to keep your Docker environment tidy. It acts as a digital compost heap, identifying and gracefully (or not-so-gracefully, depending on your mood) disposing of stale, exited containers and dangling images. By converting this digital detritus into "compost," it helps maintain a healthy, efficient system, freeing up disk space and reducing clutter.

## How it Works

This utility runs as a Docker container itself. To interact with your Docker daemon, it requires access to the Docker socket (`/var/run/docker.sock`). It then uses standard `docker` CLI commands to inspect, list, and optionally prune containers and images.

## Usage

To use the `nightly-container-compost`, you'll run it as a Docker container, mounting your Docker socket.

### Dry Run (Recommended First)

Always start with a dry run to see what would be composted without actually deleting anything.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-container-compost:latest --dry-run
```

Example Output (Dry Run):

```
🌿 Initiating Nightly Container Compost Cycle... 🌿

Scanning for digital detritus...

Found 2 stale containers ready for composting:
  - Container ID: a1b2c3d4e5f6, Name: old_web_server, Status: Exited (0) 2 weeks ago
  - Container ID: f6e5d4c3b2a1, Name: forgotten_db, Status: Exited (137) 3 days ago

Found 2 dangling images ready for composting:
  - Image ID: 1234567890ab, Repository: <none>, Tag: <none> (Size: 150MB)
  - Image ID: abcdef123456, Repository: <none>, Tag: <none> (Size: 50MB)

Total potential compost: 2 containers, 2 images.
This was a dry run. No actual composting performed.
Run with '--prune' to fertilize your system!
```

### Prune (Compost!)

Once you're satisfied with the dry run report, you can proceed with actual composting. **Use with caution!** This will permanently remove the identified containers and images.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-container-compost:latest --prune
```

Example Output (Prune):

```
🌿 Initiating Nightly Container Compost Cycle... 🌿

Scanning for digital detritus...

Found 2 stale containers ready for composting:
  - Container ID: a1b2c3d4e5f6, Name: old_web_server, Status: Exited (0) 2 weeks ago
  - Container ID: f6e5d4c3b2a1, Name: forgotten_db, Status: Exited (137) 3 days ago

Found 2 dangling images ready for composting:
  - Image ID: 1234567890ab, Repository: <none>, Tag: <none> (Size: 150MB)
  - Image ID: abcdef123456, Repository: <none>, Tag: <none> (Size: 50MB)

Proceeding with composting...

--- Container Prune Log ---
Deleted Containers:
a1b2c3d4e5f6
f6e5d4c3b2a1
Total reclaimed space: 100MB
--- Image Prune Log ---
Deleted Images:
1234567890ab
abcdef123456
Total reclaimed space: 200MB

✨ Compost Report: ✨
  - Containers pruned: 2
  - Images pruned: 2
Your Docker garden is now refreshed and ready for new growth!
```

## Building the Image

To build the Docker image yourself:

```bash
docker build -t nightly-container-compost:latest .
```

## Development & Testing

The `compost.sh` script is a simple bash script. Tests are written in bash and use a mocked `docker` command to ensure determinism and offline execution.
