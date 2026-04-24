# Nightly Docker Environment Manager

This utility provides a whimsical yet practical way to manage isolated development environments using Docker. It allows you to quickly spin up containers pre-configured with common development tools, ensuring consistency and reproducibility across projects.

## Philosophy

"Build it once, run it anywhere, break it safely." This tool embraces the power of containers to create ephemeral, disposable development sandboxes. Think of it as a portable toolbox for your coding adventures.

## Features

*   **Pre-defined Environments**: Easily launch containers with common stacks (e.g., Node.js, Python, Go).
*   **Customizable Images**: Extend the base images to include your specific project dependencies.
*   **Isolated Workspaces**: Keep your development environments clean and free from system-wide conflicts.
*   **Ephemeral by Design**: Spin up, work, and tear down without leaving a trace on your host system.

## Usage

### 1. Build the Docker Image

Navigate to the `docker-env-manager` directory and build the Docker image:

```bash
docker build -t apoc-env-manager .
```

### 2. Run a Development Environment

To start a new environment, use the `docker run` command. You can specify the desired image tag and mount your project directory.

**Example: Launching a Python environment**

```bash
docker run -it --rm -v $(pwd):/app -w /app apoc-env-manager:latest python
```

*   `-it`: Interactive terminal.
*   `--rm`: Automatically remove the container when it exits.
*   `-v $(pwd):/app`: Mounts the current directory on your host to `/app` inside the container.
*   `-w /app`: Sets the working directory inside the container to `/app`.
*   `apoc-env-manager:latest`: The name of the Docker image.
*   `python`: The command to run inside the container (e.g., `python`, `node`, `go`).

### 3. Customizing Environments

Modify the `Dockerfile` to include additional tools or specific versions of software. For instance, to add `git` and `curl` to the Python image:

```dockerfile
# ... existing Dockerfile content ...

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

Then, rebuild the image.

## Testing

Unit tests are included to verify the functionality of the Dockerfile and the basic commands. Run them using `docker build` and then execute the test script within a container.

```bash
# Build the image with tests
docker build --target test -t apoc-env-manager-test .

# Run the tests (this will be handled by the Dockerfile's test stage)
```
