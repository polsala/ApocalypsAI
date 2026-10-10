# nightly-digital-dust-bunny

## 🧹 Digital Dust Bunny Sweeper 🧹

This whimsical utility helps you keep your Docker environment tidy by identifying "digital dust bunnies" – unused and forgotten Docker images, containers, and volumes. It scans your system and provides a friendly report, guiding you on how to sweep them away.

Think of it as a little robot vacuum for your Docker daemon, pointing out the clutter without actually cleaning it up for you (safety first!).

## ✨ Features

*   **Identifies Dangling Images**: Finds images that are no longer tagged and are taking up space.
*   **Locates Exited Containers**: Lists containers that have finished their job and are just sitting there.
*   **Detects Dangling Volumes**: Points out volumes that are not associated with any container.
*   **Whimsical Reporting**: Presents findings in a fun, easy-to-understand format.
*   **Safe Operation**: Only reports; does not perform any destructive actions itself. Provides clear instructions for manual cleanup.

## 🚀 How to Use

### 1. Build the Docker Image

First, you need to build the `nightly-digital-dust-bunny` Docker image. Navigate to the utility's directory and run:

```bash
docker build -t nightly-digital-dust-bunny .
```

### 2. Run the Sweeper

To run the sweeper, you need to mount your Docker daemon's socket into the container. This allows the utility to communicate with your Docker environment.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-digital-dust-bunny
```

The `--rm` flag ensures the container is automatically removed after it exits.

### 3. Interpret the Report

The utility will print a report to your console, listing any digital dust bunnies it finds.

Example output:

```
✨ Welcome to the Digital Dust Bunny Sweeper! ✨
Scanning your Docker environment for forgotten bits and bobs...
--------------------------------------------------
🧹 Oh dear! I've found 3 digital dust bunnies lurking around:
  - 1 dangling image (like forgotten socks behind the dryer):
    - Image ID: 1a2b3c4d5e6f
  - 1 exited container (like empty snack wrappers):
    - Container Name: old-web-server
  - 1 dangling volume (like lost keys under the couch):
    - Volume Name: forgotten_data_vol
--------------------------------------------------
To sweep these digital dust bunnies away, run:
  docker system prune --volumes
This command will remove all stopped containers, all networks not used by at least one container,
all dangling images, and optionally all dangling volumes.
Use with caution! Always review what will be removed before confirming.
```

If your environment is clean, you'll get a celebratory message!

### 4. Sweep Away the Dust Bunnies (Optional)

If the report indicates dust bunnies, you can use the recommended `docker system prune` command to clean them up. **Always review the output of `docker system prune` before confirming, as it performs destructive actions.**

```bash
docker system prune --volumes
```

## 🧪 Development and Testing

### Prerequisites

*   Docker installed and running on your system.
*   Python 3.x (for local development/testing of `app.py` if not using Docker).

### Running Tests

The tests are implemented as a Bash script that builds the Docker image, creates specific test resources (dangling images, exited containers, dangling volumes), runs the `nightly-digital-dust-bunny` container, and then verifies its output. Finally, it cleans up all test-related resources.

To run the tests, navigate to the utility's directory and execute:

```bash
./tests/test_dust_bunny.sh
```

This script requires Docker to be running and accessible.
