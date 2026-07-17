## Nightly Docker Env Manager

A whimsical yet useful utility for managing isolated Dockerized development environments.

This tool allows you to quickly spin up and tear down pre-defined development environments using Docker Compose. It's designed to be self-contained and easy to use, perfect for trying out new projects or ensuring consistent development setups.

### Features

*   **Pre-defined Environments**: Easily define and manage multiple development environments.
*   **Isolation**: Each environment runs in its own Docker container, preventing conflicts.
*   **Speed**: Quick startup and teardown of environments.
*   **Simplicity**: A straightforward command-line interface.

### Usage

1.  **Build the Docker image**: 
    ```bash
    docker build -t apocalypsai/docker-env-manager .
    ```

2.  **Run the manager**: 
    ```bash
    docker run --rm -v $(pwd)/environments:/app/environments -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/docker-env-manager <command> [environment_name]
    ```

    *   `--rm`: Automatically remove the container when it exits.
    *   `-v $(pwd)/environments:/app/environments`: Mounts your local `environments` directory into the container, allowing you to define your environments there.
    *   `-v /var/run/docker.sock:/var/run/docker.sock`: Grants the container access to the Docker daemon on your host.

    **Available Commands**: 
    *   `up <environment_name>`: Starts a specified environment.
    *   `down <environment_name>`: Stops and removes a specified environment.
    *   `list`: Lists all available environments.
    *   `status <environment_name>`: Shows the status of a specified environment.

    **Example**: To start a Python development environment named `python-dev`:
    ```bash
    docker run --rm -v $(pwd)/environments:/app/environments -v /var/run/docker.sock:/var/run/docker.sock apocalypsai/docker-env-manager up python-dev
    ```

3.  **Define your environments**: 
    Create `.yaml` files in the `environments` directory (or a directory you mount to `/app/environments`). These files should be valid Docker Compose configurations.

    **Example `environments/python-dev.yaml`**:
    ```yaml
    version: '3.8'
    services:
      python_app:
        image: python:3.9-slim
        volumes:
          - .:/app
        working_dir: /app
        command: tail -f /dev/null # Keep container running
    ```

### Testing

Run the tests using `docker-compose run --rm app test` within the container.

### Contributing

Feel free to add new environment definitions to the `environments` directory or suggest improvements to the manager itself!
