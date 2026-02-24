# Nightly Temporal Echo Chamber

A containerized utility for recording and replaying the outputs of arbitrary commands, allowing for deterministic testing and simulation of past execution.

## 🌌 Overview

The `Nightly Temporal Echo Chamber` captures the standard output, standard error, exit code, and execution duration of any command run within its confines. This "echo" can then be replayed, faithfully reproducing the original command's behavior, including its output streams and exit status. This is invaluable for:

*   **Deterministic Testing**: Create stable test fixtures for CLI tools or scripts that interact with external, non-deterministic services (e.g., network calls, random data generation, timestamps).
*   **Offline Development**: Simulate complex environments or long-running processes without needing live dependencies.
*   **Debugging**: Replay specific command failures to analyze their exact output and exit conditions.
*   **Temporal Distortion**: Optionally introduce delays during replay to simulate network latency or slow operations.

## 🚀 Usage

The utility is provided as a Docker image.

### 📦 Build the Docker Image

First, build the Docker image from the provided `Dockerfile`:

```bash
docker build -t temporal-echo-chamber .
```

### ✍️ Record a Command's Echo

To record a command, use the `record` subcommand. You need to specify an output JSON file where the echo will be stored, followed by the command you wish to record.

```bash
# Example: Record a simple command
docker run --rm -v "$(pwd):/app" temporal-echo-chamber record /app/my_command_echo.json bash -c "echo 'Hello from the past!'; sleep 0.1; echo 'Error from the void!' >&2; exit 7"

# Explanation:
# --rm: Automatically remove the container when it exits.
# -v "$(pwd):/app": Mounts your current directory into the container at /app,
#                   allowing the output JSON file to be written to your host machine.
# temporal-echo-chamber: The name of the Docker image.
# record: The subcommand to capture an echo.
# /app/my_command_echo.json: The path inside the container where the echo will be saved.
# bash -c "...": The actual command to be recorded.
```

After execution, `my_command_echo.json` will contain a JSON object similar to this:

```json
{
  "command": ["bash", "-c", "echo 'Hello from the past!'; sleep 0.1; echo 'Error from the void!' >&2; exit 7"],
  "timestamp": "2023-10-27T10:30:00Z",
  "duration_seconds": 0.123,
  "stdout": "Hello from the past!\n",
  "stderr": "Error from the void!\n",
  "exit_code": 7
}
```

### 👂 Replay a Recorded Echo

To replay a previously recorded command's echo, use the `replay` subcommand and provide the path to the JSON echo file. The utility will print the recorded stdout and stderr, and exit with the recorded exit code.

```bash
# Example: Replay the previously recorded command
docker run --rm -v "$(pwd):/app" temporal-echo-chamber replay /app/my_command_echo.json

# You can also add a delay factor to simulate longer operations:
docker run --rm -v "$(pwd):/app" temporal-echo-chamber replay /app/my_command_echo.json --delay-factor 2.5
```

The replay will output "Hello from the past!" to stdout, "Error from the void!" to stderr, and the `docker run` command itself will exit with code `7`. If `--delay-factor 2.5` was used, it would wait `0.123 * 2.5` seconds before outputting.

## 🛠️ Development

### Prerequisites

*   Docker
*   `bash`
*   `jq` (for inspecting JSON files)

### Running Tests

The tests are implemented as a `bash` script that builds a temporary Docker image and runs the `echo_chamber.sh` script in both `record` and `replay` modes, verifying the outputs and exit codes.

```bash
./tests/test_echo_chamber.sh
```

This will:
1.  Create a temporary `Dockerfile.test` and a `dummy_cmd.sh`.
2.  Build a Docker image named `temporal-echo-chamber-test`.
3.  Run `echo_chamber.sh record` with `dummy_cmd.sh` inside the container, saving output to `echo_output.json`.
4.  Verify the contents of `echo_output.json`.
5.  Run `echo_chamber.sh replay` with `echo_output.json`.
6.  Verify the replayed stdout, stderr, and exit code.
7.  Clean up all temporary files and Docker artifacts.
