# Nightly Digital Dust Bunny Sweeper

## Summary

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful containerized utility designed to keep your Docker environment pristine by automatically pruning old and unused Docker images, volumes, and networks. Think of it as a tiny, diligent robot sweeping away the digital dust bunnies that accumulate over time, freeing up disk space and maintaining system hygiene.

## Usage

This utility is designed to run as a Docker container, connecting to your host's Docker daemon to perform cleanup operations. It requires access to the Docker socket.

### 1. Build the Docker Image

Navigate to the utility's directory and build the image:

```bash
docker build -t digital-dust-bunny-sweeper .
```

### 2. Run the Sweeper

You can run the sweeper manually or schedule it using a cron job. The container needs to mount the Docker socket from the host to interact with the Docker daemon.

**Basic Run (prune all older than 24 hours):**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock digital-dust-bunny-sweeper
```

**Specify Mode and Age Threshold:**

The utility accepts two optional arguments:
1.  `MODE`: What to prune. Options: `all` (default), `images`, `volumes`, `networks`.
2.  `AGE`: The age threshold for pruning. Docker's `--filter "until=..."` format (e.g., `24h`, `7d`, `30m`). Default is `24h`.

**Examples:**

*   **Prune only old images (older than 7 days):**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock digital-dust-bunny-sweeper images 7d
    ```

*   **Prune old volumes (older than 30 minutes):**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock digital-dust-bunny-sweeper volumes 30m
    ```

*   **Prune all (system prune) older than 1 week:**
    ```bash
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock digital-dust-bunny-sweeper all 7d
    ```

### 3. Schedule with Cron (Example)

To run the sweeper daily at 3:00 AM, you can add an entry to your crontab (`crontab -e`):

```cron
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock digital-dust-bunny-sweeper all 24h > /var/log/dust-bunny-sweeper.log 2>&1
```

This will prune all Docker resources older than 24 hours every day at 3 AM and log the output to `/var/log/dust-bunny-sweeper.log`.
