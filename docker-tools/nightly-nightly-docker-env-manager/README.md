## Nightly Docker Env Manager

A whimsical yet useful utility for managing isolated development environments using Docker. This tool allows you to quickly spin up, tear down, and list your custom Docker-based development environments.

### Philosophy

"Containerize your chaos, tame your dependencies." This utility embraces the power of Docker to provide reproducible and isolated development spaces, ensuring your local setup is as predictable as a well-oiled apocalypse bunker.

### Features

*   **`start <env_name>`**: Starts a new development environment based on a predefined Docker image and configuration.
*   **`stop <env_name>`**: Stops and removes a running development environment.
*   **`list`**: Lists all currently running development environments managed by this tool.
*   **`status <env_name>`**: Shows the status of a specific development environment.
*   **`logs <env_name>`**: Displays the logs for a specific development environment.

### Usage

1.  **Build the Docker image**: `docker build -t apocalypsai/env-manager .`
2.  **Run the manager**: `docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/env-manager <command> [args]`

**Example Commands:**

*   Start a Python 3.10 environment named `py310-dev`:
    `docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/env-manager start py310-dev --image python:3.10-slim`

*   Stop the `py310-dev` environment:
    `docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/env-manager stop py310-dev`

*   List all environments:
    `docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/env-manager list`

### Configuration

Environments are defined by a `docker-compose.yml` file within the `envs/` directory. The `start` command will look for a corresponding `docker-compose.yml` for the given environment name.

**Example `envs/py310-dev.yml`:**

```yaml
version: '3.8'
services:
  app:
    image: python:3.10-slim
    command: tail -f /dev/null # Keep the container running
    volumes:
      - .:/app # Mount current directory for development
```

### Testing

This utility includes integration tests that verify its functionality by interacting with the Docker daemon. These tests are designed to be deterministic and run offline by mocking Docker API calls.

Run tests using `docker-compose run --rm app pytest` within the `tests/` directory after building the main image.
