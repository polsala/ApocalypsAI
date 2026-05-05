# Nightly Ephemeral Environment Enforcer

## Summary

The `nightly-ephemeral-env-enforcer` is a robust Docker-based utility designed to manage temporary, isolated development or testing environments. It launches a specified Docker container with a given command and ensures that the container is stopped and removed after a predefined duration, preventing resource leaks and ensuring clean slate operations.

This tool is perfect for CI/CD pipelines, automated testing, or any scenario where you need to spin up a temporary service or environment and guarantee its cleanup.

## How it Works

1.  **Launch**: The utility takes a target Docker image, a duration in seconds, and a command to execute within that image.
2.  **Monitor**: It starts the target container in detached mode.
3.  **Enforce**: After the specified duration, it checks if the container is still running. If it is, the utility forcefully stops and removes it. If the container has already exited, it ensures it's removed to clean up any lingering resources.

## Build Instructions

To build the `nightly-ephemeral-env-enforcer` Docker image, navigate to the utility's directory and run:

```bash
docker build -t nightly-ephemeral-env-enforcer .
```

## Usage

To use the enforcer, you need to run its container with access to the Docker daemon (usually by mounting `/var/run/docker.sock`). Then, provide the target image, duration, and command as arguments.

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-ephemeral-env-enforcer \
  <TARGET_IMAGE> <DURATION_SECONDS> <COMMAND...>
```

**Example: Run an Nginx server for 30 seconds**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-ephemeral-env-enforcer \
  nginx:latest 30 "nginx -g 'daemon off;'"
```

**Example: Run a quick test script in Ubuntu for 10 seconds**

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  nightly-ephemeral-env-enforcer \
  ubuntu:latest 10 "bash -c 'echo Starting test...; sleep 5; echo Test complete!'"
```

**Arguments:**

*   `<TARGET_IMAGE>`: The Docker image to launch (e.g., `ubuntu:latest`, `nginx:stable`).
*   `<DURATION_SECONDS>`: The maximum number of seconds the target container is allowed to run before being stopped and removed.
*   `<COMMAND...>`: The command to execute inside the target container. This should typically be a long-running command or a script that simulates work.

## Automated Tests

The utility includes a self-contained test script that mocks Docker commands to ensure deterministic and offline verification of its logic.

To run the tests, you can execute the `test_entrypoint.sh` script directly within the built Docker image:

```bash
docker run --rm nightly-ephemeral-env-enforcer /app/tests/test_entrypoint.sh
```

Alternatively, if you have the source files, you can run the test script directly (after making it executable):

```bash
chmod +x tests/test_entrypoint.sh
./tests/test_entrypoint.sh
```

Note: Running `test_entrypoint.sh` directly outside the container requires the `entrypoint.sh` script to be available at `/app/entrypoint.sh` or adjusted paths. The `docker run` command above is the recommended way to test the built image's behavior.
