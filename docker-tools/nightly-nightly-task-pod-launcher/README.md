# Nightly Task Pod Launcher

The `nightly-task-pod-launcher` is a whimsical-yet-useful utility designed to provide a temporary, isolated Docker environment for executing single commands. Think of it as a disposable workbench: you spin it up, run your task, and it vanishes without a trace, keeping your local environment pristine.

This tool is perfect for:
- Running a command with a specific tool or language version not installed on your host.
- Testing a script in a clean, isolated environment.
- Executing one-off tasks without cluttering your system with dependencies.
- Experimenting with new tools without permanent installation.

## Usage

To use the Task Pod Launcher, you need Docker installed and running on your system.

```bash
./src/task_pod.sh <DOCKER_IMAGE> "<COMMAND_TO_EXECUTE>"
```

- `<DOCKER_IMAGE>`: The name of the Docker image to use (e.g., `ubuntu:latest`, `python:3.10-slim`, `alpine/git`).
- `<COMMAND_TO_EXECUTE>`: The command you want to run inside the container. **Ensure this is quoted if it contains spaces or special characters.**

The current working directory on your host will be mounted into `/workspace` inside the container, and the command will be executed from `/workspace`. This allows your containerized task to interact with files in your current project.

### Examples

1. **Check Python version using a specific image:**
   ```bash
   ./src/task_pod.sh python:3.10-slim "python --version"
   ```

2. **Run a Node.js script without Node.js installed locally:**
   (Assuming you have `my_script.js` in your current directory)
   ```bash
   # Create a dummy script for demonstration
   echo "console.log('Hello from Node.js in a pod!');" > my_script.js
   ./src/task_pod.sh node:18-alpine "node my_script.js"
   rm my_script.js # Clean up dummy script
   ```

3. **Compile a C program in a temporary GCC environment:**
   (Assuming you have `hello.c` in your current directory)
   ```bash
   # Create a dummy C program
   echo '#include <stdio.h>\nint main() { printf("Hello from C in a pod!\\n"); return 0; }' > hello.c
   ./src/task_pod.sh gcc:latest "gcc hello.c -o hello && ./hello"
   rm hello.c hello # Clean up dummy files
   ```

4. **Run a quick `git` command with `alpine/git`:**
   ```bash
   ./src/task_pod.sh alpine/git "git status"
   ```

## How it Works

The script leverages Docker's `--rm` flag, which automatically removes the container and its filesystem when the container exits. It also mounts your current host directory as `/workspace` inside the container, making it easy to work with local files. The command is executed via `/bin/sh -c` to ensure proper shell interpretation.

## Development and Testing

### Prerequisites

- Docker (for actual execution, not for tests)
- Bash

### Running Tests

The tests for this utility use a mocked `docker` command to ensure they are deterministic and do not require a running Docker daemon.

```bash
./tests/test_task_pod.sh
```

This will execute the test suite, verifying that the `task_pod.sh` script correctly constructs and attempts to run Docker commands, and handles exit codes as expected.
