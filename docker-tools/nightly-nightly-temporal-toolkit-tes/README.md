# Nightly Temporal Toolkit Tesseract

## Summary

The `nightly-temporal-toolkit-tesseract` is a whimsical-yet-useful containerized development environment. It comes pre-loaded with a suite of essential CLI tools, designed to provide a stable and consistent workspace for rapid deployment, troubleshooting, and even responding to unexpected temporal anomalies or system collapses. Think of it as your go-to survival kit for any digital wasteland.

## Features

*   **Pre-installed Tools**: Includes `git`, `curl`, `wget`, `jq`, `yq`, `vim`, `tmux`, `htop`, `net-tools`, `ping`, `ansible`, `terraform`, `kubectl`, and `awscli`.
*   **Isolated Environment**: Runs in a Docker container, ensuring a consistent environment regardless of your host system.
*   **Rapid Deployment**: Get a fully equipped shell up and running with a single `docker run` command.
*   **Whimsical Naming**: Because even in the apocalypse, a little humor goes a long way.

## Usage

### 1. Build the Docker Image

Navigate to the `src` directory and build the Docker image:

```bash
cd nightly-temporal-toolkit-tesseract/src
docker build -t temporal-toolkit-tesseract .
```

### 2. Run the Container

Once built, you can run the container to get an interactive bash shell:

```bash
docker run -it temporal-toolkit-tesseract
```

This will drop you into a bash shell inside the container, where all the pre-installed tools are available.

### 3. Execute Specific Commands

You can also execute specific commands directly within the container without entering an interactive shell:

```bash
docker run --rm temporal-toolkit-tesseract git --version
docker run --rm temporal-toolkit-tesseract terraform version
```

### 4. Mount Local Volumes (Optional)

To work with your local files inside the container, you can mount a volume:

```bash
docker run -it -v "$(pwd)":/workspace temporal-toolkit-tesseract
```

This command mounts your current host directory into `/workspace` inside the container, allowing you to edit files with `vim` or run `git` commands on your local repository.

## Included Tools

The Tesseract comes equipped with:

*   `git`: Version control
*   `curl`, `wget`: Network requests
*   `jq`, `yq`: JSON and YAML processing
*   `vim`: Text editor
*   `tmux`: Terminal multiplexer
*   `htop`: Process viewer
*   `net-tools`, `iputils-ping`: Network diagnostics
*   `ansible`: Automation engine
*   `terraform`: Infrastructure as Code
*   `kubectl`: Kubernetes CLI
*   `awscli`: AWS Command Line Interface

## Development & Contribution

Feel free to expand the toolkit with more essential utilities! Just modify the `Dockerfile` and ensure tests pass.
