# Nightly Wanderer's Portable Workshop

A self-contained, lightweight Docker image designed to provide a quick and consistent development environment for "wasteland wanderers" (developers) on the go. It bundles essential CLI tools and a simple HTTP server, making it perfect for rapid prototyping, sharing files, or running small scripts without polluting your host system.

## Features

*   **Lightweight**: Built on Alpine Linux for a minimal footprint.
*   **Essential Tools**: Includes `bash`, `python3`, `nano`, `vim`, `curl`, `jq`.
*   **File Sharing**: Easily share files from your host machine into the container via volume mounts, and serve them via a built-in Python HTTP server.
*   **Flexible Entrypoint**: Run a shell, execute a specific command, or start the HTTP server by default.

## Usage

### Build the Docker Image

Navigate to the `nightly-wanderer-workshop` directory and build the image:

```bash
docker build -t wanderer-workshop .
```

### Run the Workshop (Default: HTTP Server)

By default, running the container without a command will start a Python HTTP server on port 8000, serving files from the current working directory inside the container.

```bash
docker run -p 8000:8000 -v "$(pwd):/app" wanderer-workshop
```

Now, open your browser to `http://localhost:8000` to see your current directory's contents.

### Run a Shell Inside the Workshop

To get an interactive shell with all the bundled tools:

```bash
docker run -it -v "$(pwd):/app" wanderer-workshop bash
```

You can then use `python3`, `nano`, `jq`, `curl`, etc., within this isolated environment.

### Execute a Specific Command

Run any command directly:

```bash
docker run -v "$(pwd):/app" wanderer-workshop python3 -c "print('Hello from the workshop!')"
docker run -v "$(pwd):/app" wanderer-workshop jq --version
```

## Included Tools

*   `bash`
*   `python3` (with `pip`)
*   `nano`
*   `vim`
*   `curl`
*   `jq`
*   Python's `http.server` (default command)

## Development

To contribute or modify, simply edit the `Dockerfile` or `src/entrypoint.sh` and rebuild the image.
