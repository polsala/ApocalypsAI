# Nightly Chrono-Container Courier

## Summary

The `nightly-chrono-container-courier` is a whimsical-yet-useful Docker-based utility designed to execute scripts or commands within a temporary, isolated container environment of your choosing. Think of it as sending your code through a 'temporal conduit' to run in a specific past, present, or alternate future environment defined by a Docker image.

This is particularly useful for:
*   **Reproducible Script Execution**: Ensure your scripts run consistently regardless of your host's environment.
*   **Dependency Testing**: Test scripts against specific versions of interpreters or libraries (e.g., Python 3.8 vs 3.10, Node.js 14 vs 18).
*   **Clean Sandboxing**: Run untrusted or experimental code without polluting your local system.
*   **Cross-Platform Compatibility**: Verify scripts behave as expected on different base operating systems (e.g., Alpine, Ubuntu).

## How it Works

The courier itself is a lightweight Docker container. When you run it, it leverages your host's Docker daemon to launch *another* temporary container (the 'temporal' environment) based on the `TARGET_IMAGE` you specify. Your current working directory is mounted into this target container at `/app`, allowing your scripts to be accessible and executed.

## Usage

1.  **Build the Courier Image (once)**:
    ```bash
    docker build -t nightly-chrono-container-courier .
    ```

2.  **Run the Courier**:
    To use the courier, you need to:
    *   Mount your host's Docker socket (`/var/run/docker.sock`) into the courier container so it can control other containers.
    *   Mount your current working directory (`$(pwd)`) into the courier container as `/app_host_mount`. This directory will then be passed through to the target container as `/app`.
    *   Specify the `TARGET_IMAGE` (e.g., `python:3.9-slim`, `node:16-alpine`).
    *   Provide the command and its arguments that you want to execute *inside* the `TARGET_IMAGE`.

    ```bash
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v "$(pwd)":/app_host_mount \
      nightly-chrono-container-courier \
      <TARGET_IMAGE> [COMMAND_AND_ARGS_FOR_TARGET_CONTAINER...]
    ```

    **Example 1: Running a Python script**
    Assume you have `my_script.py` in your current directory:
    ```python
    # my_script.py
    import sys
    print(f"Hello from Python {sys.version.split(' ')[0]} in a container!")
    print(f"Arguments received: {sys.argv[1:]}")
    ```
    Execute it with Python 3.9:
    ```bash
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v "$(pwd)":/app_host_mount \
      nightly-chrono-container-courier \
      python:3.9-slim python /app/my_script.py arg1 arg2
    ```

    **Example 2: Running a Bash command in an older Ubuntu environment**
    ```bash
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v "$(pwd)":/app_host_mount \
      nightly-chrono-container-courier \
      ubuntu:18.04 bash -c "echo 'Current OS:' && cat /etc/os-release"
    ```

    **Example 3: Passing environment variables to the target container**
    ```bash
    docker run --rm \
      -v /var/run/docker.sock:/var/run/docker.sock \
      -v "$(pwd)":/app_host_mount \
      nightly-chrono-container-courier \
      alpine:latest -e MY_SECRET_VAR=apocalypse_key sh -c 'echo "My secret is: $MY_SECRET_VAR"'
    ```

## Development & Testing

To run the automated tests, execute:

```bash
bash tests/test_courier.sh
```

These tests use a mock Docker environment to ensure determinism and avoid requiring a live Docker daemon during testing.
