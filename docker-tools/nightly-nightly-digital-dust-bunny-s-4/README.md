# Nightly Digital Dust Bunny Sweeper

## Summary

The `nightly-digital-dust-bunny-sweep` is a whimsical-yet-powerful containerized utility designed to keep your Docker environment sparkling clean. It identifies and prunes old, unused Docker images, volumes, networks, and build cache, preventing digital "dust bunnies" from accumulating and consuming precious disk space.

## How it Works

This utility runs a Bash script inside a Docker container. It requires access to the host's Docker daemon (via `/var/run/docker.sock`) to perform its cleaning magic. Based on configurable environment variables, it intelligently executes `docker prune` commands with appropriate filters.

It can target:
- **Dangling Images**: Images not associated with any container.
- **Unused Images**: Images older than a specified age.
- **Unused Volumes**: Volumes not attached to any container.
- **Unused Networks**: Networks not used by any running container.
- **Build Cache**: Stale build cache entries.

By default, it runs in a dry-run mode, reporting what *would* be cleaned without making any changes.

## Configuration

The sweeper's behavior is controlled by environment variables:

- `DRY_RUN` (default: `true`): Set to `false` to perform actual cleanup. Any other value (including `true`) will result in a dry run.
- `MAX_AGE_HOURS` (default: `24`): Prune images, volumes, and networks older than this many hours.
- `CLEANUP_IMAGES` (default: `true`): Set to `false` to skip image cleanup.
- `CLEANUP_VOLUMES` (default: `true`): Set to `false` to skip volume cleanup.
- `CLEANUP_NETWORKS` (default: `true`): Set to `false` to skip network cleanup.
- `CLEANUP_BUILD_CACHE` (default: `true`): Set to `false` to skip build cache cleanup.

## Usage

1.  **Build the Docker image (optional, or pull from a registry):**
    ```bash
    docker build -t digital-dust-bunny-sweeper .
    ```

2.  **Run the sweeper (Dry Run - Recommended first!):**
    This command mounts your Docker socket, allowing the container to interact with your host's Docker daemon.
    ```bash
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      digital-dust-bunny-sweeper
    ```
    *Output will show what *would* be cleaned.*

3.  **Run the sweeper (Actual Cleanup):**
    ```bash
    docker run --rm \
      -e DRY_RUN=false \
      -v /var/run/docker.sock:/var/run/docker.sock \
      digital-dust-bunny-sweeper
    ```
    *This will actually remove resources! Use with caution.*

4.  **Customizing Cleanup (Example: Clean only images older than 7 days):**
    ```bash
    docker run --rm \
      -e DRY_RUN=false \
      -e MAX_AGE_HOURS=168 \
      -e CLEANUP_VOLUMES=false \
      -e CLEANUP_NETWORKS=false \
      -e CLEANUP_BUILD_CACHE=false \
      -v /var/run/docker.sock:/var/run/docker.sock \
      digital-dust-bunny-sweeper
    ```

## Example Output (Dry Run)

```
🧹 ApocalypsAI Digital Dust Bunny Sweeper is waking up... 🧹
🔍 Scanning for digital dust bunnies (Dry Run mode active!). No actual sweeping will occur.
⏳ Looking for images older than 24 hours...
    [DRY RUN] Would run: docker image prune --filter "until=24h" --format '{{.ID}} {{.Repository}}:{{.Tag}}'
    [DRY RUN] Would run: docker image prune --filter "dangling=true" --format '{{.ID}} {{.Repository}}:{{.Tag}}'
⏳ Looking for volumes older than 24 hours...
    [DRY RUN] Would run: docker volume prune --filter "until=24h" --format '{{.Name}}'
⏳ Looking for networks older than 24 hours...
    [DRY RUN] Would run: docker network prune --filter "until=24h" --format '{{.Name}}'
⏳ Looking for build cache remnants...
    [DRY RUN] Would run: docker builder prune --all --filter "until=24h"
✨ Dry run complete! Your Docker environment *would* be much tidier. ✨
To perform actual cleanup, run with -e DRY_RUN=false.
```
