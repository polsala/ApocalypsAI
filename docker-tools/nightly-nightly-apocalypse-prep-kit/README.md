# nightly-apocalypse-prep-kit

A whimsical-yet-useful containerized "Apocalypse Prep Kit" that provides a temporary, isolated environment with essential CLI tools for quick, isolated tasks. Think of it as your go-to sandbox for when your main development environment is acting up, or you just need a clean slate for a quick script or file manipulation.

## Features

*   **Isolated Environment**: Runs in a Docker container, keeping your host system clean.
*   **Essential CLI Tools**: Includes `bash`, `git`, `nano`, `less`, `tar`, `gzip`, `unzip`, `curl`, `wget`, `jq`, `grep`, `sed`, `awk`, `python3`, and `pip`.
*   **Ephemeral**: The container is removed automatically after you exit, leaving no trace.
*   **Volume Mounting**: Automatically mounts your current working directory into `/workspace` inside the container, allowing you to easily access and modify your local files.

## Usage

1.  **Ensure Docker is Running**: Make sure Docker Desktop or your Docker daemon is active on your system.

2.  **Navigate to Your Project Directory**:
    Change your current directory to where you want to work. This directory will be mounted into the container.

    ```bash
    cd /path/to/your/project
    ```

3.  **Run the Prep Kit**:
    Execute the `run.sh` script located in the `src/` directory of this utility.

    ```bash
    /path/to/this/utility/nightly-apocalypse-prep-kit/src/run.sh
    ```

    Alternatively, if you are in the `nightly-apocalypse-prep-kit` directory:

    ```bash
    ./src/run.sh
    ```

    This will build the Docker image (if not already built) and then drop you into a `bash` shell inside the container. Your current host directory will be accessible at `/workspace`.

4.  **Work Inside the Container**:
    You can now use any of the pre-installed tools. For example:

    ```bash
    # List files in your mounted directory
    ls -l /workspace

    # Edit a file
    nano /workspace/my_script.py

    # Start a simple Python web server to serve files from /workspace (accessible from within the container)
    python3 -m http.server 8000
    ```
    (Note: To access a web server from your host, you would need to add `-p <host_port>:<container_port>` to the `docker run` command in `run.sh`. For simplicity and isolation, this utility focuses on CLI tools and local file access within the container.)

5.  **Exit the Container**:
    Simply type `exit` and press Enter. The container will automatically stop and be removed.

## Development & Testing

### Prerequisites

*   Docker installed and running.
*   Bash shell.

### Building the Image Manually

If you just want the Docker image without running the interactive shell:

```bash
docker build -t apocalypsai-prep-kit ./src
```

### Running Tests

Navigate to the utility's root directory and execute the test script:

```bash
./tests/test_prep_kit.sh
```

This script will build a test image, run a temporary container, and verify that all expected tools are present and the `/workspace` directory is set up correctly.
