# Nightly Temporal Dev Chamber

## Overview

The `nightly-temporal-dev-chamber` is a whimsical-yet-useful utility designed to help developers manage and interact with isolated, version-locked development environments. Ever had a project that only 'works on my machine (from 5 years ago)'? Or needed to test compatibility with an ancient runtime? The Temporal Dev Chamber allows you to quickly spin up a containerized 'chamber' with specific operating system versions, language runtimes, and tools, ensuring a consistent and reproducible environment for debugging, testing, or just reminiscing about simpler times.

It's like a time machine for your development setup, without the paradoxes (mostly).

## Features

*   **Isolated Environments**: Each chamber is a Docker container, completely isolated from your host system.
*   **Version Locking**: Easily specify OS, language, and tool versions for precise environment replication.
*   **Simple Management**: A `chamber_manager.sh` script provides commands to build, run, enter, list, and clean up your temporal chambers.
*   **Extensible**: Customize `Dockerfile`s to include any specific tools or libraries your legacy projects require.

## Prerequisites

*   Docker installed and running on your system.
*   A bash-compatible shell.

## Usage

### 1. Build a Temporal Chamber Image

First, you need to define your chamber's environment using a `Dockerfile`. The provided `src/Dockerfile` is a generic base that can be extended or used as a template. You can pass build arguments to customize it.

```bash
# Example: Build a Python 3.6 chamber based on Ubuntu 18.04
./src/chamber_manager.sh build python-3-6-chamber src/Dockerfile --build-arg OS_VERSION=ubuntu:18.04 --build-arg PYTHON_VERSION=3.6

# Example: Build a Node.js 10 chamber
./src/chamber_manager.sh build node-10-chamber src/Dockerfile --build-arg OS_VERSION=ubuntu:20.04 --build-arg NODE_VERSION=10
```

**Note**: The `src/Dockerfile` is a basic template. For specific language versions, you might need to modify it or create a new `Dockerfile` that installs the exact version you need (e.g., using `pyenv`, `nvm`, or specific apt repositories).

### 2. Enter a Temporal Chamber

Once an image is built, you can enter it to get an interactive shell:

```bash
./src/chamber_manager.sh enter python-3-6-chamber
# You are now inside the container, e.g., for Python 3.6
# (python3 --version should show 3.6.x)
```

### 3. Run a Command in a Chamber

Execute a specific command without entering an interactive shell:

```bash
./src/chamber_manager.sh run python-3-6-chamber "python3 -c 'print(\"Hello from the past!\")'"
```

### 4. List Available Chambers

See all temporal chamber images you've built:

```bash
./src/chamber_manager.sh list
```

### 5. Clean Up a Chamber

Remove a chamber image to free up space:

```bash
./src/chamber_manager.sh clean python-3-6-chamber
```

## Customizing Your Chambers

The `src/Dockerfile` is a starting point. For more complex or specific environments:

1.  **Create a new `Dockerfile`**: Copy `src/Dockerfile` to a new location (e.g., `my-chambers/Dockerfile.legacy-app`) and modify it to install your specific dependencies.
2.  **Build with your custom Dockerfile**: `chamber_manager.sh build my-legacy-chamber my-chambers/Dockerfile.legacy-app`

This allows you to tailor each chamber precisely to the needs of your legacy projects.

## Development & Testing

Tests are located in `tests/test_chamber_manager.sh` and use a mocked Docker environment to ensure deterministic and offline execution. Run them with:

```bash
./tests/test_chamber_manager.sh
```
