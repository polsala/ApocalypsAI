# Nightly Chrono-Gardener

A whimsical, containerized utility designed to keep your Docker environment pristine by periodically pruning stale images, stopped containers, and unused networks. Think of it as a diligent digital gardener, ensuring your container ecosystem doesn't get overgrown with digital weeds!

## 🌿 Features

*   **Automated Pruning**: Sweeps away unused Docker resources.
*   **Volume Management**: Optionally prunes unused volumes to reclaim even more space.
*   **Dry Run Mode**: Preview what would be pruned without making any changes.
*   **Containerized**: Runs as a lightweight Docker container, easily integrated into scheduled tasks (e.g., cron jobs, GitHub Actions).
*   **Whimsical Output**: Enjoy delightful messages as your digital garden gets tidied up.

## 🚀 Usage

The Chrono-Gardener runs as a Docker container. You'll need Docker installed on your host system.

### 1. Build the Docker Image

First, build the `nightly-chrono-gardener` image:

```bash
docker build -t nightly-chrono-gardener .
```

### 2. Run the Gardener

To run the gardener, you need to mount the Docker socket from your host system into the container. This allows the container's `docker-cli` to interact with the host's Docker daemon.

#### Default Pruning (Containers, Images, Networks - no Volumes)

This will prune stopped containers, dangling images, and unused networks. Unused volumes will be preserved.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-chrono-gardener
```

#### Pruning with Volumes

To include unused volumes in the pruning process, set the `PRUNE_VOLUMES` environment variable to `true`:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e PRUNE_VOLUMES="true" nightly-chrono-gardener
```

#### Dry Run Mode

To see what would be pruned without actually making any changes, set the `DRY_RUN` environment variable to `true`:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e DRY_RUN="true" nightly-chrono-gardener
# Or with volumes in dry run:
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e DRY_RUN="true" -e PRUNE_VOLUMES="true" nightly-chrono-gardener
```

### 3. Schedule with Cron (Example)

For automated, periodic gardening, you can set up a cron job on your host system.

To run the gardener every day at 3:00 AM (pruning volumes):

```bash
# Add this line to your crontab (crontab -e)
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -e PRUNE_VOLUMES="true" nightly-chrono-gardener >> /var/log/chrono-gardener.log 2>&1
```

Remember to replace `/var/log/chrono-gardener.log` with your desired log file path.

## 🛠️ Development

### Running Tests

To run the automated tests, execute the `test_gardener.sh` script:

```bash
bash tests/test_gardener.sh
```

These tests use a mocked `docker` command to ensure determinism and prevent actual system changes during testing.

## 📜 License

This project is licensed under the MIT License.
