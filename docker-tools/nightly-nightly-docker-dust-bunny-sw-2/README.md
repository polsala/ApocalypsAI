# Nightly Docker Dust Bunny Sweeper

## Summary

The `nightly-docker-dust-bunny-sweeper` is a whimsical-yet-useful containerized utility designed to keep your Docker environment sparkling clean by automatically identifying and sweeping away "digital dust bunnies." These dust bunnies manifest as exited containers, dangling (untagged) images, and unused dangling volumes that accumulate over time, consuming precious disk space and cluttering your system.

This tool runs a series of targeted `docker` cleanup commands to ensure your Docker daemon remains efficient and tidy, preventing the digital equivalent of finding a forgotten sock under the server rack.

## How it Works

The utility runs a simple bash script inside a Docker container. This script connects to your host's Docker daemon (via a mounted socket) and executes the following cleanup operations:

1.  **Sweeps Exited Containers**: Removes all containers that have stopped running.
2.  **Sweeps Dangling Images**: Removes all images that are not associated with any tagged repositories and are not used by any running containers.
3.  **Sweeps Dangling Volumes**: Removes all volumes that are not currently attached to any containers.

## Usage

To use the Nightly Docker Dust Bunny Sweeper, you need to have Docker installed and running on your system.

### 1. Build the Docker Image (Optional, or use a pre-built one)

Navigate to the utility's directory and build the Docker image:

```bash
docker build -t nightly-docker-dust-bunny-sweeper .
```

### 2. Run the Sweeper

The sweeper needs access to your Docker daemon's socket to perform its magic. You can run it as follows:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-dust-bunny-sweeper
```

*   `--rm`: Automatically remove the container when it exits.
*   `-v /var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker daemon's socket from your host into the container, allowing the script inside to interact with your Docker environment. **Caution**: Granting access to the Docker socket is powerful. Ensure you trust the container's script.

### 3. Schedule for Nightly Cleanups (Optional)

For true "nightly" integration, you can schedule this command using `cron` on Linux/macOS or Task Scheduler on Windows.

**Example Cron Job (Linux/macOS):**

To run the sweeper every night at 3:00 AM, add the following line to your crontab (`crontab -e`):

```cron
0 3 * * * docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-docker-dust-bunny-sweeper > /var/log/docker-sweeper.log 2>&1
```

This will run the command, redirecting its output to a log file for review.

## Development and Testing

### Prerequisites

*   Bash
*   Docker (for building and running the container)

### Running Tests

The tests for this utility are designed to be deterministic and do not require a live Docker daemon. They achieve this by mocking the `docker` command.

To run the tests:

```bash
bash tests/test_sweeper.sh
```

This script will set up a mock `docker` executable in a temporary directory, run the `dust_bunny_sweeper.sh` script under different scenarios (with and without "dust bunnies"), and verify its output.

## Contributing

Feel free to contribute to making your Docker environment even cleaner and more whimsical!
