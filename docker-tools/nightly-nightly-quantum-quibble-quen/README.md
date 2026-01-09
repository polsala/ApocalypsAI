# Nightly Quantum Quibble Quencher

## Summary
The `nightly-quantum-quibble-quencher` is a whimsical yet practical utility designed to provide a safe, isolated environment for executing arbitrary commands or scripts. Think of it as a pocket dimension where your potentially 'quibbling' (conflicting or unstable) commands can run without disturbing the delicate balance of your host system. It leverages Docker to create ephemeral containers, ensuring a clean slate for each execution.

## Features
- **Isolation**: Runs commands in a dedicated Docker container, preventing interference with your host system.
- **Ephemeral**: Containers are automatically removed after execution, leaving no trace.
- **Simple Interface**: Execute any command or script with a straightforward command-line interface.
- **Whimsical Reporting**: Provides a status report on whether your 'quibble' was successfully 'quenched' or if 'temporal ripples' were observed.

## Usage

1.  **Ensure Docker is running**: The utility relies on a running Docker daemon.

2.  **Make the script executable**:
    ```bash
    chmod +x src/quibble_quencher.sh
    ```

3.  **Run a command**: Pass the command and its arguments directly to the `quibble_quencher.sh` script.

    **Example 1: A simple, successful command**
    ```bash
    ./src/quibble_quencher.sh echo "Hello from the Quibble Quencher!"
    ```
    Expected Output:
    ```
    Initiating Quibble Quencher protocol for: echo Hello from the Quibble Quencher!
    ------------------------------------------------
    Hello from the Quibble Quencher!
    ------------------------------------------------
    Quibble Quencher Report:
    Command: echo Hello from the Quibble Quencher!
    Exit Code: 0
    Status: Quibble successfully quenched. Reality remains stable.
    Quibble Quencher session complete. Purging temporal residue...
    ```

    **Example 2: A command that exits with an error**
    ```bash
    ./src/quibble_quencher.sh sh -c 'echo "Oh no, a temporal anomaly!" >&2; exit 1'
    ```
    Expected Output:
    ```
    Initiating Quibble Quencher protocol for: sh -c echo "Oh no, a temporal anomaly!" >&2; exit 1
    ------------------------------------------------
    Oh no, a temporal anomaly!
    ------------------------------------------------
    Quibble Quencher Report:
    Command: sh -c echo "Oh no, a temporal anomaly!" >&2; exit 1
    Exit Code: 1
    Status: Quibble detected! Temporal ripples observed. Exit code indicates anomaly.
    Quibble Quencher session complete. Purging temporal residue...
    ```

    **Example 3: Running a more complex script (e.g., Python)**
    ```bash
    ./src/quibble_quencher.sh python3 -c 'import sys; print("Python says hi!"); sys.exit(0)'
    ```
    *(Note: The base Alpine image might not have python3 by default. For commands requiring specific dependencies, you might need to modify `src/Dockerfile` to install them or use a different base image, e.g., `ubuntu:latest` or `python:alpine`)*

## Development

### Building the Docker Image
The utility automatically builds its minimal `alpine:latest` based Docker image (`quibble-quencher-runtime`) on the first run if it doesn't exist locally. You can also build it manually from the `src/` directory:
```bash
cd src/
docker build -t quibble-quencher-runtime -f Dockerfile .
cd ..
```

## Tests
To run the automated tests, execute the test script:
```bash
./tests/test_quibble_quencher.sh
```

These tests use a mocked `docker` command to ensure determinism and avoid requiring a live Docker daemon during testing. They verify the script's argument parsing, output handling, and exit code propagation.
