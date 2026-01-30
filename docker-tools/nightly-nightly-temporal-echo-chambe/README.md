# Nightly Temporal Echo Chamber

## Summary
Ever needed to debug a bug that only appears in the "ancient past" of your software stack? The Temporal Echo Chamber allows you to spin up isolated Docker containers pre-configured with specific historical environments. Revisit bygone eras of dependencies, operating systems, or toolchains to understand and resolve temporal distortions in your code.

This utility provides a flexible Docker setup to create and manage these isolated environments, enabling you to test compatibility, reproduce bugs, or simply explore different software versions without affecting your host system.

## Usage

1.  **Build an Echo Chamber Era:**
    To create a new historical environment (an "era"), specify a unique tag and optionally the Python version you wish to use. The default Python version is `3.9`.
    ```bash
    ./src/echo_chamber.sh build <era_tag> [python_version]
    # Example: Build an environment with Python 3.7 tagged as 'ancient-py37'
    ./src/echo_chamber.sh build ancient-py37 3.7
    # Example: Build an environment with default Python (3.9) tagged as 'default-era'
    ./src/echo_chamber.sh build default-era
    ```

2.  **Enter/Run a Command in an Echo Chamber Era:**
    Once an era is built, you can run commands inside its container. If no command is specified, it will drop you into a `bash` shell.
    ```bash
    ./src/echo_chamber.sh run <era_tag> [command...]
    # Example: Check the Python version in the 'ancient-py37' era
    ./src/echo_chamber.sh run ancient-py37 "python --version"
    # Example: Start an interactive bash session in the 'default-era'
    ./src/echo_chamber.sh run default-era
    ```

3.  **Clean Up an Echo Chamber Era:**
    Remove the Docker image associated with a specific era to free up disk space.
    ```bash
    ./src/echo_chamber.sh cleanup <era_tag>
    # Example: Remove the 'ancient-py37' image
    ./src/echo_chamber.sh cleanup ancient-py37
    ```

## Configuration & Customization

The core of the Temporal Echo Chamber is the `Dockerfile`. You can modify it to:

*   Change the base image (`FROM`) to a different operating system or distribution.
*   Install additional tools, libraries, or dependencies specific to your desired historical environment.
*   Add custom configuration files or scripts that should be present in the chamber.

By default, the `Dockerfile` installs `git`, `curl`, and `vim` for basic utility within any era.
