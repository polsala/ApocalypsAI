## Nightly Docker Env Manager

A whimsical yet practical utility for managing isolated development environments using Docker. This tool allows you to define and launch pre-configured development environments with ease, ensuring consistency and reproducibility across projects.

### Philosophy

"Containerize your chaos, orchestrate your code." This utility embraces the power of Docker to create ephemeral, reproducible development spaces, keeping your main system clean and your projects isolated.

### Features

*   **Environment Definitions**: Define your development environments in simple YAML files.
*   **Quick Launch**: Spin up a new environment with a single command.
*   **Clean Teardown**: Effortlessly remove environments when you're done.
*   **Customizable Images**: Use existing Docker images or build your own.

### Usage

1.  **Define an Environment**: Create a `env.yaml` file in your project directory.

    ```yaml
    name: my-python-dev
    image: python:3.11-slim
    ports:
      - "8000:8000"
    volumes:
      - ".:/app"
    commands:
      - "pip install -r requirements.txt"
    ```

2.  **Build the Docker Image (Optional)**: If you need a custom image, create a `Dockerfile`.

    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    ```

3.  **Run the Manager**: Use the `docker-env-manager` command.

    *   **Launch**: `docker-env-manager up` (will look for `env.yaml` in the current directory)
    *   **Stop**: `docker-env-manager down`
    *   **Logs**: `docker-env-manager logs <container_name>`

### Installation

Build the Docker image and run the container.

```bash
docker build -t apoc-env-manager .
docker run -it --rm -v "$(pwd):/app" apoc-env-manager up
```

### Testing

Tests are included to verify the functionality of the manager. Run them using `docker-compose run --rm app pytest`.
