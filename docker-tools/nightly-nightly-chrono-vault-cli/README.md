# Nightly Chrono-Vault CLI

## Your Time-Traveling Toolkit for Temporal Anomalies

The Nightly Chrono-Vault CLI is a whimsical-yet-robust containerized toolkit designed for the discerning survivor, temporal anomaly investigator, or anyone needing a consistent set of essential command-line utilities. In a world of shifting realities and unpredictable system states, the Chrono-Vault provides a stable, isolated environment with core tools for data manipulation, integrity checks, and basic system diagnostics.

Think of it as your trusty multi-tool, always ready, always consistent, regardless of the host system's chaotic whims.

### Features

*   **Isolated Environment**: Runs in a Docker container, ensuring consistent behavior across different operating systems.
*   **Essential CLI Tools**: Bundles `nano`, `base64`, `sha256sum`, `tar`, `date`, `jq`, and `curl`.
*   **Whimsical Theme**: Framed as a toolkit for navigating temporal distortions and data corruption.
*   **Easy to Use**: Simple `run_vault.sh` script to build and launch.

### Included Tools

*   `nano`: A friendly text editor for quick edits.
*   `base64`: Encode and decode data for secure (or just obfuscated) transmission.
*   `sha256sum`: Verify the integrity of your precious data caches.
*   `tar`: Archive and extract files, essential for preserving historical records.
*   `date`: Keep track of temporal shifts and synchronize your chronometers.
*   `jq`: Process JSON data, because even in the apocalypse, APIs persist.
*   `curl`: Fetch data from the remnants of the internet or local network beacons.

### Usage

1.  **Ensure Docker is installed**: You'll need Docker Desktop or Docker Engine running on your system.

2.  **Build the Chrono-Vault image**: 
    Navigate to the `nightly-chrono-vault-cli` directory and run:
    ```bash
    ./src/run_vault.sh build
    ```
    This will build the Docker image named `chrono-vault-cli`.

3.  **Enter the Chrono-Vault**:
    To launch an interactive shell within the Chrono-Vault:
    ```bash
    ./src/run_vault.sh run
    ```
    You will be dropped into a bash shell inside the container, where all the included tools are available.

    Example:
    ```bash
    # Inside the container
    echo "Temporal Anomaly Detected!" | base64
    # Output: VGltcG9yYWwgQW5vbWFseSBEZXRlY3RlZCEK
    ```

4.  **Execute a single command**:
    To run a specific command within the Chrono-Vault without entering an interactive shell:
    ```bash
    ./src/run_vault.sh exec "echo 'Current temporal epoch:' && date"
    ```
    This will execute the command and exit the container.

### Development & Testing

To run the automated tests, ensure Docker is running, then execute:
```bash
./tests/test_vault.sh
```
The tests will verify that the Docker image builds correctly and that all specified tools are present and functional within the container.
