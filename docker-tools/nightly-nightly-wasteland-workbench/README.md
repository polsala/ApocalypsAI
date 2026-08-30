# Nightly Wasteland Workbench

A containerized, portable development workbench for the post-apocalyptic developer, complete with essential tools and survival tips.

## Overview

In the desolate future, a reliable set of tools is paramount. The "Nightly Wasteland Workbench" provides a lightweight, consistent, and isolated development environment, bundled as a Docker image. It's designed for quick scripting, data manipulation, and general utility tasks, ensuring you always have your essentials, no matter how chaotic the digital landscape becomes.

Upon launching, you'll be greeted with a whimsical survival tip to keep your spirits high in the face of impending doom.

## Features

*   **Essential CLI Tools**: `git`, `curl`, `jq`, `python3`, `pip`.
*   **Isolated Environment**: Prevents dependency conflicts and ensures reproducibility.
*   **Whimsical Survival Tips**: A dose of humor and wisdom with every session.
*   **Lightweight**: Built on Alpine Linux for minimal footprint.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-wasteland-workbench` directory and build the image:

```bash
docker build -t wasteland-workbench .
```

### 2. Run the Workbench

To launch an interactive shell within the workbench:

```bash
docker run -it wasteland-workbench
```

You will be greeted by the entrypoint script, a survival tip, and then dropped into a `/bin/bash` shell.

To run a specific command within the workbench:

```bash
docker run --rm wasteland-workbench python3 -c "print('Hello from the wasteland!')"
docker run --rm wasteland-workbench jq --version
```

### 3. Mount Volumes (Optional)

To work with local files inside the container, mount your current directory:

```bash
docker run -it -v "$(pwd):/app" -w /app wasteland-workbench
```

Now, any files in your host's current directory will be accessible under `/app` inside the container.

## Development

### Directory Structure

```
.
├── README.md
├── Dockerfile
├── src/
│   └── entrypoint.sh
└── tests/
    └── test_workbench.sh
```

### `Dockerfile`

Defines the base image, installs necessary tools, and sets up the entrypoint.

### `src/entrypoint.sh`

The script executed when the container starts. It displays the welcome message and survival tip before handing control to the specified command or a default shell.

## Testing

To run the automated tests, ensure Docker is running on your system.

```bash
bash tests/test_workbench.sh
```

The tests will build the image, run it with various commands, and assert the expected output.
