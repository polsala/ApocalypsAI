# Nightly Docker Echo Replay

The `nightly-docker-echo-replay` is a whimsical-yet-useful utility designed to capture the output of commands run within Docker containers and "replay" them later. This allows you to simulate past container executions without needing the actual Docker environment or the time taken for the original command. It's perfect for demonstrations, testing scripts that depend on specific command outputs, or creating reproducible "snapshots" of container behavior.

## Features

*   **Record Mode**: Execute a command in any specified Docker image and save its standard output, standard error, and exit code to a JSON file.
*   **Replay Mode**: Read a previously recorded JSON file and print its captured output, simulating the original command's execution.
*   **Containerized**: The tool itself runs within a Docker container, making it easy to deploy and use across different environments.

## Usage

First, build the `nightly-docker-echo-replay` Docker image:

```bash
docker build -t nightly-docker-echo-replay .
```

### 1. Record a Command's Output

To record the output of a command from another Docker image:

```bash
docker run --rm -v "$(pwd)/output:/app/output" nightly-docker-echo-replay record \
    --image "ubuntu:latest" \
    --command "bash -c 'echo Hello from Ubuntu; sleep 1; echo Error message >&2; exit 42'" \
    --output "/app/output/ubuntu_hello.json"
```

*   `--image`: The Docker image to run the command in (e.g., `ubuntu:latest`).
*   `--command`: The command to execute inside the target Docker image.
*   `--output`: The path inside the `nightly-docker-echo-replay` container where the output JSON will be saved. We use a volume mount (`-v "$(pwd)/output:/app/output"`) to persist this file to your host machine.

The `ubuntu_hello.json` file will contain the captured stdout, stderr, and exit code.

### 2. Replay Recorded Output

To replay a previously recorded output:

```bash
docker run --rm -v "$(pwd)/output:/app/output" nightly-docker-echo-replay replay \
    --input "/app/output/ubuntu_hello.json"
```

*   `--input`: The path inside the `nightly-docker-echo-replay` container to the JSON file containing the recorded output. Again, a volume mount is used to access the file from your host.

The tool will print the captured stdout, followed by stderr, simulating the original command's execution.

## Development & Testing

### Building the Docker Image

```bash
docker build -t nightly-docker-echo-replay .
```

### Running Tests

The tests are designed to run offline and mock Docker interactions.

```bash
docker run --rm -v "$(pwd)/tests:/app/tests" nightly-docker-echo-replay python -m pytest /app/tests/test_echo_replay.py
```

Or, if you have Python and `pytest` installed locally:

```bash
python -m pytest tests/test_echo_replay.py
```
