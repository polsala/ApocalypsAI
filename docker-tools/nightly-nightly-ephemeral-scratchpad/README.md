# Nightly Ephemeral Scratchpad

## Summary
The `nightly-ephemeral-scratchpad` utility provides a temporary, isolated Docker container for quick command execution, script testing, or file editing. It automatically cleans up the container and any associated temporary files on your host system once your session ends, ensuring a clean development environment.

## Whimsical Origin
In the post-apocalyptic landscape, resources are scarce, and digital clutter is a luxury no one can afford. The Ephemeral Scratchpad was devised by the ApocalypsAI Integrator to offer survivors a pristine, temporary workspace, a digital canvas that vanishes without a trace, much like a fleeting whisper in the wasteland wind. It's perfect for those moments when you need to quickly test a theory, compile a small utility, or just doodle some code without leaving permanent digital footprints.

## Usage

### Prerequisites
- Docker must be installed and running on your system.

### Running the Scratchpad
1. Navigate to the `docker-tools/nightly-ephemeral-scratchpad` directory.
2. Execute the `run.sh` script:
   ```bash
   ./src/run.sh
   ```
   This will build the Docker image (if it doesn't exist) and launch an interactive `bash` shell inside the container.

### Passing Commands Directly
You can also pass commands directly to the scratchpad, which will execute them and then exit:
```bash
./src/run.sh echo "Hello from the ephemeral scratchpad!"
./src/run.sh python -c "print('Python is here!')"
```

### Inside the Scratchpad
- Your current working directory on the host will be mounted as `/scratchpad/current_dir` inside the container (read-only).
- A temporary directory on your host will be mounted as `/scratchpad/host_mount`. Any files you create or modify in `/scratchpad/host_mount` will persist on your host at the temporary location until the container exits and the cleanup script runs.
- The container comes pre-installed with `bash`, `vim`, `git`, `curl`, `jq`, `yq`, `nano`, and `build-base` (for basic compilation).

### Automatic Cleanup
When you exit the `bash` shell (e.g., by typing `exit` or pressing `Ctrl+D`) or when the direct command finishes, the container will automatically stop and be removed. The temporary directory created on your host for `/scratchpad/host_mount` will also be deleted.

## How it Works
The `run.sh` script performs the following steps:
1. **Docker Check**: Verifies that Docker is installed and accessible.
2. **Image Build**: Checks if the `apocalypsai/ephemeral-scratchpad` Docker image exists. If not, it builds it from the `Dockerfile` in the current directory.
3. **Temporary Directory**: Creates a unique temporary directory on your host system. This directory is used to persist any files you might create or modify within the container's `/scratchpad/host_mount` during your session, allowing you to retrieve them before the final cleanup.
4. **Container Launch**: Starts a new Docker container with:
   - Interactive TTY (`-it`) for a shell experience.
   - Automatic removal on exit (`--rm`).
   - Your current host directory mounted read-only to `/scratchpad/current_dir`.
   - The temporary host directory mounted to `/scratchpad/host_mount`.
   - The default command is `bash`, but you can override it by passing arguments to `run.sh`.
5. **Cleanup**: A `trap` ensures that when the `run.sh` script exits (after the container finishes), the temporary host directory is recursively deleted.

## Development and Testing

### Building the Docker Image Manually
```bash
docker build -t apocalypsai/ephemeral-scratchpad .
```

### Running Tests
Navigate to the `docker-tools/nightly-ephemeral-scratchpad` directory and run:
```bash
./tests/test_scratchpad.sh
```
The tests use shell script mocking to simulate Docker commands and verify the script's logic without requiring a live Docker daemon.
