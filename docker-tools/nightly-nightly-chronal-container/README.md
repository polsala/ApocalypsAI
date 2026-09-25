# Nightly Chronal Container

## Overview

The `nightly-chronal-container` is a whimsical-yet-useful Docker-based utility designed to transport your command-line executions into a "temporal echo" of a past system environment. Ever needed to test an old script against an older Python version, or debug a legacy application that only runs on a specific Ubuntu release? This tool provides a self-contained, isolated environment to do just that, without polluting your current development setup.

By default, it's configured to simulate an Ubuntu 20.04 (Focal Fossa) environment, complete with its default package versions. You can easily customize the `Dockerfile` to define your own specific "past" – whether it's an even older OS, a different distribution, or a precise set of library versions.

## Features

*   **Isolated Execution**: Run commands in a clean, containerized environment.
*   **Temporal Echo**: Default configuration provides an Ubuntu 20.04 base.
*   **Customizable Past**: Easily modify the `Dockerfile` to define any desired historical environment.
*   **Simple Interface**: Just build the image and run your command.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-chronal-container` directory and build the Docker image. You can tag it with a memorable name, like `chronal-container`:

```bash
docker build -t chronal-container .
```

### 2. Run Commands in the Chronal Container

Once the image is built, you can run any command inside it. The container's entrypoint will execute whatever you pass to `docker run`.

**Example: Check Python version in the past environment**

```bash
docker run --rm chronal-container python3 --version
```

Expected output (for Ubuntu 20.04):

```
Python 3.8.10
```

**Example: Run a bash shell in the past environment**

If you don't provide a command, it defaults to `bash`, allowing you to interactively explore the past environment:

```bash
docker run -it --rm chronal-container
```

**Example: Execute a custom script (by mounting a volume)**

To run a script from your host machine within the container, you can mount your current directory as a volume:

```bash
docker run --rm -v "$(pwd)":/app chronal-container bash -c "ls -l /app && python3 /app/your_script.py"
```

### 3. Customize Your Temporal Echo

To simulate a different past, simply edit the `Dockerfile`:

*   **Change Base Image**: Modify the `FROM` instruction (e.g., `FROM debian:stretch`, `FROM centos:7`).
*   **Install Specific Versions**: Use `apt-get install <package>=<version>` or `pip install <package>==<version>` to pin dependencies.
*   **Add Tools**: Install any other tools or libraries required for your specific historical context.

After modifying the `Dockerfile`, remember to rebuild the image:

```bash
docker build -t my-custom-past-container .
```

## Development and Testing

### Automated Tests

To ensure the Chronal Container builds correctly and its entrypoint functions as expected, run the provided test script:

```bash
bash tests/test_chronal_container.sh
```

This script will:
1.  Build the Docker image.
2.  Run `python3 --version` inside the container and verify the output (expecting Python 3.8 for Ubuntu 20.04).
3.  Run a simple `bash -c "echo ..."` command to test the default entrypoint behavior.
4.  Clean up the created Docker image.

### Cleaning Up

To remove the built Docker image manually:

```bash
docker rmi chronal-container
```

(Replace `chronal-container` with your image tag if you used a different one.)
