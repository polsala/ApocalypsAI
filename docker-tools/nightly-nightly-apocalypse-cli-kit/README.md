# Nightly Apocalypse CLI Kit

A containerized, whimsical-yet-useful command-line interface (CLI) toolbox designed for the discerning survivor of the digital wasteland. This utility provides a curated set of essential CLI tools within an isolated Docker container, ensuring you always have your favorite utilities handy, regardless of your host system's state.

## Features

*   **Isolated Environment**: Run critical CLI operations without polluting your host system.
*   **Curated Toolset**: Includes `bash`, `curl`, `wget`, `jq`, `grep`, `sed`, `awk`, `openssl`, `netcat`, `git`, `vim`, `tree`.
*   **Whimsical Prompt**: A custom shell prompt to remind you of your apocalyptic mission.
*   **Portable**: Easily deployable on any system with Docker.

## Usage

### Build the Docker Image

Navigate to the `nightly-apocalypse-cli-kit` directory and build the image:

```bash
docker build -t apocalypse-cli-kit .
```

### Run the Toolbox

To enter the survival shell:

```bash
docker run -it apocalypse-cli-kit
```

You will be greeted by a custom prompt `(ApocalypseKit):/app$` (or similar, depending on your current directory within the container).

To run a specific command within the toolbox without entering an interactive shell:

```bash
docker run apocalypse-cli-kit curl --version
docker run apocalypse-cli-kit git status
```

### Mount Volumes (Optional)

To work with files from your host system, you can mount a volume:

```bash
docker run -it -v "$(pwd):/data" apocalypse-cli-kit bash
# Now you can access your host's current directory contents under /data inside the container.
```

## Included Tools

*   `bash`: The ubiquitous shell.
*   `curl`: Transfer data with URLs.
*   `wget`: Non-interactive network downloader.
*   `jq`: Lightweight and flexible command-line JSON processor.
*   `grep`, `sed`, `awk`: Powerful text processing utilities.
*   `openssl`: Toolkit for SSL/TLS protocols and cryptography.
*   `netcat`: Simple Unix utility that reads and writes data across network connections.
*   `git`: The distributed version control system.
*   `vim`: A highly configurable text editor.
*   `tree`: List contents of directories in a tree-like format.

## Contributing

Feel free to suggest more essential tools for the post-apocalyptic world!
