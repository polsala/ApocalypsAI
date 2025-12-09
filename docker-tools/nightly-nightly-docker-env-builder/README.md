## Nightly Docker Env Builder

This utility provides a quick and easy way to spin up a pre-configured Docker environment for your development projects. It allows you to specify a list of common development tools to be installed within the container, ensuring a consistent and reproducible setup.

### Features

*   **Containerized Environment**: All tools are isolated within a Docker container.
*   **Customizable Tooling**: Specify the tools you need (e.g., `git`, `node`, `python`, `docker-cli`, `kubectl`, `aws-cli`).
*   **Reproducible Builds**: Ensures everyone on the team has the same development environment.
*   **Fast Setup**: Get up and running with your project dependencies quickly.

### Usage

1.  **Build the Docker image:**
    ```bash
    docker build -t apoc-dev-env .
    ```

2.  **Run the container and mount your project directory:**
    ```bash
    docker run -it --rm -v $(pwd):/app -w /app apoc-dev-env bash
    ```
    *   `-it`: Interactive terminal.
    *   `--rm`: Remove the container when it exits.
    *   `-v $(pwd):/app`: Mounts your current directory to `/app` inside the container.
    *   `-w /app`: Sets the working directory to `/app`.

3.  **Inside the container, you'll have access to the installed tools.**

### Customization

To customize the tools installed, modify the `TOOLS_TO_INSTALL` variable in the `Dockerfile`.

### Example `Dockerfile` snippet:

```dockerfile
# ... other Dockerfile content ...

ARG TOOLS_TO_INSTALL="git node python docker-cli kubectl aws-cli"

RUN apt-get update && apt-get install -y --no-install-recommends \
    $TOOLS_TO_INSTALL \
    && rm -rf /var/lib/apt/lists/*

# ... rest of Dockerfile ...
```

### Testing

Run the provided tests to ensure the Docker image builds correctly and the specified tools are available.

```bash
docker build -t apoc-dev-env .
docker run --rm apoc-dev-env which git
docker run --rm apoc-dev-env which node
# ... and so on for other tools ...
```
