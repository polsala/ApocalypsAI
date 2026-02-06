# Nightly Docker Env Builder

This utility provides a convenient way to spin up isolated, reproducible development environments using Docker. It's designed to be whimsical yet practical, allowing you to quickly set up a sandbox for trying out new tools or projects without cluttering your main system.

## Features

*   **Containerized Isolation**: Runs in a Docker container, ensuring a clean and isolated environment.
*   **Customizable Environments**: Easily define your desired environment (e.g., Python, Node.js, Go) via a simple configuration file.
*   **Reproducibility**: Ensures that your development environment is the same every time you build it.
*   **Whimsical Touch**: Because even in the apocalypse, we can have fun with our tools!

## Usage

1.  **Build the Docker Image**:
    ```bash
    docker build -t apocalypsai/docker-env-builder .
    ```

2.  **Create a Configuration File**:
    Create a `env_config.yaml` file in the same directory as your `docker-compose.yml` (or specify a path).

    **Example `env_config.yaml` for a Python environment:**
    ```yaml
    environment_name: python-dev
    base_image: python:3.10-slim
    packages:
      - pip
      - requests
      - beautifulsoup4
    commands:
      - echo "Welcome to your Python dev environment!"
      - python --version
    ```

    **Example `env_config.yaml` for a Node.js environment:**
    ```yaml
    environment_name: node-dev
    base_image: node:18-alpine
    packages:
      - npm
      - yarn
    commands:
      - echo "Hello, Node.js world!"
      - node -v
    ```

3.  **Run the Builder**:
    You can run the builder directly using `docker run` or integrate it into a `docker-compose.yml`.

    **Using `docker run`:**
    ```bash
    docker run --rm -v $(pwd)/env_config.yaml:/app/env_config.yaml -v $(pwd):/workspace apocalypsai/docker-env-builder
    ```
    This command will:
    *   Mount your `env_config.yaml` into the container.
    *   Mount your current directory (`$(pwd)`) to `/workspace` inside the container, allowing you to access generated files.
    *   The `--rm` flag ensures the container is removed after execution.

    The utility will create a new directory named after `environment_name` in your current directory, containing a `Dockerfile` and a `docker-compose.yml` for your new environment.

## Development and Testing

This utility is built using Python and Docker. Tests are included to ensure its functionality.

To run the tests:

1.  Ensure you have Docker installed and running.
2.  Navigate to the utility's directory.
3.  Run the test script:
    ```bash
    ./run_tests.sh
    ```

## Contributing

Feel free to fork this repository and submit pull requests with new features or improvements!
