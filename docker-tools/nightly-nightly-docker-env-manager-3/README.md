## Nightly Docker Env Manager

This utility provides a simple, containerized way to manage isolated development environments. It leverages Docker to quickly spin up and tear down pre-defined environments, ensuring consistency and reproducibility.

### Features

*   **Isolation**: Each environment runs in its own container.
*   **Reproducibility**: Define environments using Dockerfiles.
*   **Simplicity**: Easy-to-use CLI for managing environments.

### Usage

1.  **Build the Docker image**: 
    ```bash
    docker build -t apoc-env-manager .
    ```

2.  **Create an environment definition (e.g., `my-python-env.Dockerfile`)**:
    ```dockerfile
    # Example: A Python 3.10 development environment
    FROM python:3.10-slim
    RUN pip install --no-cache-dir requests
    WORKDIR /app
    ```

3.  **Start an environment**: 
    ```bash
    docker run -d --name my-python-dev -v $(pwd):/app apoc-env-manager --dockerfile my-python-env.Dockerfile --command "tail -f /dev/null"
    ```
    This command starts a detached container named `my-python-dev`, mounts the current directory, uses the `apoc-env-manager` image, builds a temporary image from `my-python-env.Dockerfile`, and keeps the container running with `tail -f /dev/null`.

4.  **Access the environment**: 
    ```bash
    docker exec -it my-python-dev bash
    ```

5.  **Stop and remove an environment**: 
    ```bash
    docker stop my-python-dev
    docker rm my-python-dev
    ```

### Advanced Usage

*   **Custom Commands**: You can specify a different command to run when starting the container.
*   **Volume Mounting**: Use the `-v` flag with `docker run` to mount local directories into the container.

### Testing

Run the tests using `docker-compose up --build`.
