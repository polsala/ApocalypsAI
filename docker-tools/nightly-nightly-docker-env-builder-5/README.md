## Nightly Docker Env Builder

This utility provides a whimsical yet practical way to spin up isolated development environments using Docker. Forget dependency hell and "it works on my machine" woes! This tool lets you define your desired environment in a simple configuration file and launches it in a clean, reproducible container.

### Features

*   **Containerized Isolation**: Each environment runs in its own Docker container, preventing conflicts.
*   **Customizable Environments**: Define your preferred programming languages, tools, and versions.
*   **Reproducibility**: Ensure everyone on your team has the exact same development setup.
*   **Quick Setup**: Get a new development environment up and running in minutes.

### Usage

1.  **Build the Docker Image**:
    ```bash
    docker build -t apoc-env-builder .
    ```

2.  **Create a Configuration File**:
    Create a `env.yaml` file in the same directory. Here's an example:

    ```yaml
    name: python-web-dev
    image: ubuntu:latest
    packages:
      - python3
      - python3-pip
      - git
      - curl
    tools:
      - name: nodejs
        version: "18"
      - name: docker-compose
        version: "latest"
    ports:
      - "8000:8000"
    volumes:
      - ".:/app"
    ```

3.  **Run the Environment**:
    ```bash
    docker run --rm -it -v $(pwd)/env.yaml:/app/env.yaml -p 8000:8000 apoc-env-builder --config env.yaml
    ```
    
    The `--rm` flag ensures the container is removed after you exit.
    The `-it` flags allow for interactive use.
    The `-v` flag mounts your current directory into the container at `/app` and the configuration file.
    The `-p` flag maps ports from the container to your host.

    You can also specify a different port mapping if needed:
    ```bash
    docker run --rm -it -v $(pwd)/env.yaml:/app/env.yaml -p 8080:8000 apoc-env-builder --config env.yaml
    ```

### Configuration Options (`env.yaml`)

*   `name`: A friendly name for your environment.
*   `image`: The base Docker image to use (e.g., `ubuntu:latest`, `python:3.9-slim`).
*   `packages`: A list of apt packages to install.
*   `tools`: A list of additional tools to install (e.g., Node.js, Docker Compose). Each tool can have a `name` and `version`.
*   `ports`: A list of port mappings in the format `HOST:CONTAINER`.
*   `volumes`: A list of volume mounts in the format `HOST_PATH:CONTAINER_PATH`.

### Development

This utility is built using a simple shell script within a Docker container. The `Dockerfile` defines the base image and installs necessary tools. The `entrypoint.sh` script parses the configuration and sets up the environment.

### Testing

Tests are included to verify the functionality of the `entrypoint.sh` script. They simulate different configuration scenarios and check for expected outcomes.
