# Nightly Chrono-Container: Temporal Anomaly Containment Unit

Ever wanted to test a suspicious script or experiment with system-altering commands without fear of polluting your host system? The Nightly Chrono-Container provides a pristine, isolated Docker environment that you can snapshot, restore, and reset at will. It's like a time machine for your command line!

## Features

*   **Isolated Execution**: Run commands in a clean, temporary environment.
*   **Snapshot/Restore**: Save and load the entire `/workspace` state, allowing you to revert to previous configurations or experiments.
*   **Ephemeral by Default**: Using `docker run --rm` ensures no lasting container footprint on your system.
*   **Persistent Snapshots**: Snapshots are stored in a host-mounted directory, allowing them to persist even if the container is removed.

## Usage

### 1. Build the Docker Image

First, navigate to the `nightly-chrono-container` directory and build the Docker image:

```bash
docker build -t chrono-container .
```

### 2. Prepare Volumes (Optional but Recommended)

For persistent work and snapshots, it's recommended to use Docker volumes or host-mounted directories:

*   **Workspace Volume**: A named Docker volume for `/workspace` will persist your files between interactive sessions.
    ```bash
docker volume create chrono_data
    ```
*   **Snapshots Directory**: A host directory to store your `.tar.gz` snapshots.
    ```bash
mkdir -p ./my_snapshots
    ```

### 3. Run Commands Ephemerally

To run a single command in a clean, temporary environment (the container is removed after execution):

```bash
docker run --rm -v $(pwd)/my_snapshots:/snapshots -v chrono_data:/workspace chrono-container bash -c "echo 'Hello from the Chrono-Container!' > /workspace/greeting.txt && cat /workspace/greeting.txt"
```

### 4. Start an Interactive Session

For an interactive shell session within the Chrono-Container:

```bash
docker run --rm -it -v $(pwd)/my_snapshots:/snapshots -v chrono_data:/workspace chrono-container bash
```

### 5. Manage Snapshots

Use the `entrypoint.sh` commands to manage your workspace state. These commands operate on the `/workspace` volume and store/retrieve snapshots from the `/snapshots` directory.

*   **Create a Snapshot**:
    ```bash
docker run --rm -it -v $(pwd)/my_snapshots:/snapshots -v chrono_data:/workspace chrono-container snapshot my_first_experiment
    ```

*   **Restore from a Snapshot**:
    ```bash
docker run --rm -it -v $(pwd)/my_snapshots:/snapshots -v chrono_data:/workspace chrono-container restore my_first_experiment
    ```

*   **List Available Snapshots**:
    ```bash
docker run --rm -it -v $(pwd)/my_snapshots:/snapshots -v chrono_data:/workspace chrono-container list-snapshots
    ```

*   **Clean Up All Snapshots**:
    ```bash
docker run --rm -it -v $(pwd)/my_snapshots:/snapshots -v chrono_data:/workspace chrono-container cleanup
    ```

## Important Notes

*   The `/workspace` directory inside the container is where your files and experiments reside. Use a Docker volume (e.g., `chrono_data`) to persist its state across container runs.
*   The `/snapshots` directory inside the container is where snapshot `.tar.gz` files are stored. It should be mounted to a host directory (e.g., `./my_snapshots`) to ensure snapshots persist even if the Docker volume for `/workspace` is removed or reset.
*   The `snapshot` command will create a compressed archive of the *entire* `/workspace` (excluding the `/snapshots` mount point itself, if it were accidentally nested). The `restore` command will clear the current `/workspace` (again, preserving `/snapshots`) and extract the archive.
