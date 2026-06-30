# Nightly Foraging Pod

## Summary
Safely explore unknown digital artifacts or test risky scripts in an isolated, ephemeral Docker container. The Foraging Pod provides a clean, temporary environment for executing commands without affecting your host system.

## Usage
To use the Foraging Pod, simply execute the `run.sh` script followed by the command you wish to run inside the container. The command should be enclosed in quotes if it contains spaces or special characters.

```bash
./src/run.sh "<command_to_run_in_container>"
```

### Examples:

*   **List files in the container's root directory:**
    ```bash
    ./src/run.sh "ls -la /"
    ```

*   **Run a simple Python script (assuming Python is installed in the container):**
    ```bash
    ./src/run.sh "python -c 'print(\"Hello from the Pod!\")'"
    ```

*   **Execute a shell command:**
    ```bash
    ./src/run.sh "echo 'Analyzing unknown artifact...' && cat /etc/os-release"
    ```

## How it Works
1.  **Builds Image**: A minimal Docker image (`foraging-pod-image`) is built using the provided `Dockerfile`.
2.  **Launches Container**: A new Docker container is launched from this image. It's named uniquely to avoid conflicts.
3.  **Executes Command**: Your specified command is executed inside the container.
4.  **Cleans Up**: Once the command completes, the container is automatically removed (`--rm`), and then the Docker image itself is deleted, leaving no trace on your system.

## Requirements
*   Docker must be installed and running on your system.
*   Bash shell for executing `run.sh`.
