## Nightly Docker Env Builder

This utility provides a quick and reproducible way to spin up development environments for various programming languages using Docker. Say goodbye to "it works on my machine" issues and hello to consistent, isolated development spaces.

### Features

*   Pre-configured Docker images for popular languages (Python, Node.js, Rust, Go).
*   Easy to extend with custom Dockerfiles.
*   Isolated environments to prevent dependency conflicts.

### Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t apoc-env-builder .
    ```

2.  **Run a new environment:**
    To start a Python 3.11 environment in a new directory called `my-python-project`:
    ```bash
    docker run --rm -v $(pwd)/my-python-project:/app -w /app apoc-env-builder python
    ```

    To start a Node.js 20 environment in a new directory called `my-node-project`:
    ```bash
    docker run --rm -v $(pwd)/my-node-project:/app -w /app apoc-env-builder node
    ```

    To start a Rust 1.70 environment in a new directory called `my-rust-project`:
    ```bash
    docker run --rm -v $(pwd)/my-rust-project:/app -w /app apoc-env-builder rust
    ```

    To start a Go 1.21 environment in a new directory called `my-go-project`:
    ```bash
    docker run --rm -v $(pwd)/my-go-project:/app -w /app apoc-env-builder go
    ```

    The command will drop you into an interactive shell within the container, with your project directory mounted at `/app`.

### Extending the Builder

To add support for a new language or a different version, simply modify the `Dockerfile` and add a corresponding entry in the `entrypoint.sh` script.

### License

This project is licensed under the MIT License - see the `LICENSE` file for details.
