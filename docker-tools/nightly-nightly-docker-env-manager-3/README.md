# Nightly Docker Environment Manager

This utility provides a whimsical yet practical way to manage isolated development environments using Docker. It allows you to quickly spin up pre-defined environments and tear them down cleanly, ensuring your main system remains pristine.

## Features

*   **Containerized Isolation**: Run your development tools and dependencies in isolated Docker containers.
*   **Pre-defined Environments**: Easily launch common development stacks (e.g., Python, Node.js, Go).
*   **Clean Teardown**: Remove all associated Docker resources with a single command.
*   **Customizable**: Extendable to support new environment definitions.

## Usage

1.  **Build the Docker image**: 
    ```bash
    docker build -t apoc-env-manager .
    ```

2.  **Spin up a Python environment**: 
    ```bash
    docker run --rm -it -v $(pwd):/app apoc-env-manager python-env
    ```
    This will start a container with Python pre-installed, mount your current directory to `/app` inside the container, and drop you into a bash shell.

3.  **Spin up a Node.js environment**: 
    ```bash
    docker run --rm -it -v $(pwd):/app apoc-env-manager node-env
    ```

4.  **Spin up a Go environment**: 
    ```bash
    docker run --rm -it -v $(pwd):/app apoc-env-manager go-env
    ```

5.  **List available environments**: 
    ```bash
    docker run --rm apoc-env-manager list-envs
    ```

## Environment Definitions

New environments can be added by creating new `Dockerfile`s in the `environments/` directory and updating the `entrypoint.sh` script to recognize them.

## Contributing

Feel free to fork this repository and add new environment definitions or improve existing ones. Open a Pull Request with your changes.
