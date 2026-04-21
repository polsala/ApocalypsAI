## Nightly Docker Env Manager

This utility provides a simple, containerized way to manage isolated development environments. It leverages Docker to quickly spin up and tear down pre-defined environments, ensuring consistency and reproducibility.

### Features

*   **Isolation**: Each environment runs in its own Docker container.
*   **Reproducibility**: Define your environment in a `Dockerfile` and `docker-compose.yml`.
*   **Simplicity**: Easy-to-use CLI for managing environments.

### Usage

1.  **Build the Docker image**: 
    ```bash
    docker build -t apoc-env-manager .
    ```

2.  **Create an environment definition**: 
    Create a directory for your environment (e.g., `my-python-env`). Inside this directory, create a `Dockerfile` and a `docker-compose.yml` file.

    **Example `my-python-env/Dockerfile`**:
    ```dockerfile
    FROM python:3.9-slim
    RUN pip install --no-cache-dir requests
    WORKDIR /app
    COPY . /app
    CMD ["python", "your_script.py"]
    ```

    **Example `my-python-env/docker-compose.yml`**:
    ```yaml
    version: '3.8'
    services:
      dev_env:
        build: .
        volumes:
          - .:/app
    ```

3.  **Start an environment**: 
    Navigate to the directory containing your environment definition and run:
    ```bash
    docker run --rm -it -v $(pwd):/app apoc-env-manager start my-python-env
    ```
    This will build the Docker image for `my-python-env` (if not already built) and start a container.

4.  **Stop an environment**: 
    The `stop` command is implicitly handled by `--rm` in the `docker run` command. For long-running services, you would typically use `docker-compose down`.

### Testing

Run the tests using `pytest`:
```bash
pytest
```

### Contributing

Feel free to contribute new environment definitions or improvements to the manager itself!
