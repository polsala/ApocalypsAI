## Nightly Docker Env Manager

A whimsical yet practical utility for managing isolated development environments using Docker. This tool allows you to quickly spin up, manage, and tear down pre-defined development environments, ensuring consistency and reproducibility.

### Philosophy

"Containerize your chaos, tame your dependencies." This utility embraces the power of Docker to create ephemeral, reproducible development spaces, freeing you from the shackles of local environment conflicts.

### Features

*   **Environment Definitions**: Define your development environments in simple YAML files.
*   **Quick Spin-up**: Launch a new environment with a single command.
*   **Clean Teardown**: Effortlessly remove environments when you're done.
*   **Isolation**: Each environment runs in its own isolated container.
*   **Reproducibility**: Ensure everyone on your team uses the exact same setup.

### Usage

1.  **Define an Environment**: Create a `environments/my-dev-env.yaml` file (see `environments/example.yaml` for structure).

    ```yaml
    name: my-python-dev
    image: python:3.10-slim
    ports:
      - "8000:8000"
    volumes:
      - ".:/app"
    commands:
      - "pip install -r requirements.txt"
    ```

2.  **Build the Docker Image (if needed)**:
    If your environment requires a custom Dockerfile, place it in the `dockerfiles/` directory and reference it in your YAML definition.

3.  **Run the Manager**: 
    ```bash
    docker run -it --rm -v "$(pwd)":/app -v /var/run/docker.sock:/var/run/docker.sock ghcr.io/polsala/apocalypsai/nightly-docker-env-manager:<tag> <command> <environment_name>
    ```

    *   **Commands**: `up`, `down`, `logs`, `exec`
    *   **Example**: `docker run ... up my-python-dev`

### Development

This utility is built using Python and Docker. The core logic resides in `src/main.py`.

### Testing

Tests are located in the `tests/` directory and are designed to be deterministic and offline.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
