# Nightly Docker Environment Manager

This utility provides a whimsical yet practical way to manage isolated development environments using Docker. It allows you to quickly spin up pre-configured environments for specific projects or tasks and tear them down cleanly when you're done.

## Features

*   **Containerized Isolation**: Each environment runs in its own Docker container, preventing conflicts.
*   **Customizable Environments**: Define your environments using simple Docker Compose files.
*   **Quick Spin-up/Tear-down**: Get your development environment ready in seconds.
*   **Clean Slate**: Easily revert to a fresh environment by destroying and recreating containers.

## Usage

1.  **Prerequisites**: Ensure you have Docker and Docker Compose installed.

2.  **Create an Environment Definition**:
    Create a `docker-compose.yml` file in a directory for your desired environment. For example, `~/dev_envs/my_python_project/docker-compose.yml`:

    ```yaml
    version: '3.8'
    services:
      app:
        image: python:3.9-slim
        volumes:
          - .:/app
        working_dir: /app
        command: tail -f /dev/null # Keep container running
    ```

3.  **Run the Manager**: 
    Navigate to the directory containing your `docker-compose.yml` file and run the `docker-env-manager` script.

    ```bash
    # From within ~/dev_envs/my_python_project/
    docker run --rm -v $(pwd):/app -w /app apocalypsai/nightly-docker-env-manager start
    ```

    This will start your Docker environment. You can then attach to it:

    ```bash
    docker exec -it <container_name_or_id> bash
    ```
    (You can find the container name/ID using `docker ps`)

4.  **Stop and Remove the Environment**: 
    When you're finished, run:

    ```bash
    docker run --rm -v $(pwd):/app -w /app apocalypsai/nightly-docker-env-manager stop
    ```

## Dockerfile

The `Dockerfile` in this repository builds a minimal image containing `docker-compose` and a simple shell script to manage the lifecycle of your environments.

## Testing

Tests are included to verify the basic functionality of the `docker-env-manager` script. They mock Docker commands to ensure deterministic and offline execution.
