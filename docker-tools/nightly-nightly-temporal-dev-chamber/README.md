# Nightly Temporal Dev Chamber

Ever had code that "worked yesterday" or "works on my machine (from 2018)"? The Nightly Temporal Dev Chamber allows you to step back in time, creating isolated Docker environments with specific language versions, dependencies, and even OS configurations. Debug temporal anomalies in your codebase with ease!

## Features

*   **Isolated Environments**: Each chamber is a self-contained Docker container.
*   **Version Locking**: Specify base images and setup commands to lock in language and dependency versions.
*   **Easy Management**: Build, run, and list your temporal chambers with simple commands.

## Usage

Navigate to the `src` directory and run the `temporal_chamber.sh` script.

### Commands:

1.  **`build <chamber_name> <base_image> [setup_commands]`**
    *   Creates a new temporal chamber image.
    *   `chamber_name`: A unique name for your chamber (e.g., `python3.8-legacy`).
    *   `base_image`: The Docker base image (e.g., `python:3.8-slim`, `node:14-alpine`).
    *   `setup_commands` (optional): A quoted string of shell commands to run during image build (e.g., `"pip install requests==2.20.0 && npm install -g yarn"`).

    **Example:**
    ```bash
    ./temporal_chamber.sh build python3.8-legacy python:3.8-slim "pip install requests==2.20.0 cryptography==2.8"
    ./temporal_chamber.sh build node14-oldie node:14-alpine "npm install -g express@4.16.0"
    ```

2.  **`run <chamber_name> [command]`**
    *   Runs a previously built temporal chamber.
    *   `chamber_name`: The name of the chamber to run.
    *   `command` (optional): The command to execute inside the container (defaults to `bash`). The current directory will be mounted to `/app` inside the container.

    **Example:**
    ```bash
    ./temporal_chamber.sh run python3.8-legacy
    ./temporal_chamber.sh run node14-oldie "node -v"
    ./temporal_chamber.sh run python3.8-legacy "python my_legacy_script.py"
    ```

3.  **`list`**
    *   Lists all currently configured temporal chambers.

    **Example:**
    ```bash
    ./temporal_chamber.sh list
    ```

## Installation

This utility requires Docker to be installed and running on your system.

1.  Clone the `polsala/ApocalypsAI` repository.
2.  Navigate to `docker-tools/nightly-temporal-dev-chamber/src`.
3.  Make the script executable: `chmod +x temporal_chamber.sh`

## Testing

To run the automated tests, navigate to the `tests` directory and execute the test script:

```bash
cd docker-tools/nightly-temporal-dev-chamber/tests
./test_temporal_chamber.sh
```

The tests use a mocked Docker environment to ensure determinism and avoid actual Docker daemon interaction.
