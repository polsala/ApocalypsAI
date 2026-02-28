# Nightly Ephemeral Dev Oasis

## Summary

The `nightly-dev-oasis` is a whimsical-yet-useful containerized utility designed to provide developers with a pristine, temporary development environment, a true 'oasis' in the vast 'wasteland' of local machine configurations. It leverages Docker Compose to spin up a set of common services (like a web server, database, and cache) with a single command, and tear them down just as easily. This ensures a consistent, isolated, and reproducible environment for testing, prototyping, or quick development tasks without polluting your host system.

## Features

*   **Quick Provisioning**: Start a multi-service development environment with a single command.
*   **Isolation**: Services run in isolated containers, preventing conflicts with local installations.
*   **Reproducibility**: Ensures consistent environments across different machines or team members.
*   **Easy Teardown**: Remove all services and associated data with another simple command.
*   **Containerized**: The utility itself runs in a Docker container, requiring only Docker to be installed on the host.

## Usage

### 1. Build the Oasis Cultivator Image

First, you need to build the `nightly-dev-oasis` Docker image. Navigate to the `nightly-dev-oasis` directory and run:

```bash
docker build -t nightly-dev-oasis .
```

### 2. Cultivate Your Oasis (Start the Environment)

To bring up your ephemeral development oasis, run the `nightly-dev-oasis` container with the `up` command. You need to mount your Docker socket so the utility can interact with the host's Docker daemon to manage other containers.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-dev-oasis up
```

This will start the default services (Nginx, PostgreSQL, Redis) defined in `src/docker-compose.yml`. You can access Nginx on `http://localhost:8080` (or the port mapped in the `docker-compose.yml`).

### 3. Check Oasis Vitality (Status)

To see the status of the services in your oasis:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-dev-oasis status
```

### 4. Wilt Your Oasis (Stop and Remove the Environment)

When you're done with your temporary environment, you can tear it down:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nightly-dev-oasis down
```

This will stop and remove all containers, networks, and volumes associated with the oasis, leaving your system clean.

### Customizing Your Oasis

The `src/docker-compose.yml` file defines the services for your oasis. You can customize this file to include different services, versions, ports, or configurations. To use a custom `docker-compose.yml`, mount it into the container at `/app/docker-compose.yml`:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v /path/to/your/custom-compose.yml:/app/docker-compose.yml nightly-dev-oasis up
```

## Development and Testing

### Running Tests

To run the automated tests for this utility, execute the `test_oasis.sh` script:

```bash
bash tests/test_oasis.sh
```

These tests use a mock `docker-compose` binary to ensure the `entrypoint.sh` script calls the correct Docker Compose commands without actually interacting with the Docker daemon during testing.
