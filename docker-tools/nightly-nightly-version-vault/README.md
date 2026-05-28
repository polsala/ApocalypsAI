# Nightly Version Vault

## Summary
The Nightly Version Vault is a whimsical-yet-useful Docker-based utility that allows you to execute commands within isolated, specified historical software environments. Ever needed to test a script against an old Python version, or debug a compatibility issue with an ancient Node.js runtime? Step into the Chrono-Container and revisit the software epochs of yore without polluting your local machine!

## Usage
To use the Version Vault, simply provide the desired Docker image and the command you wish to execute within that environment.

```bash
./nightly-version-vault <docker_image> <command...>
```

### Arguments:
*   `<docker_image>`: The Docker image tag representing the software environment you want to use (e.g., `python:3.6-slim`, `node:12-alpine`, `gcc:7`).
*   `<command...>`: The command(s) you want to run inside the container. This will be executed via `bash -c`.

### Examples:

1.  **Check an old Python version:**
    ```bash
    ./nightly-version-vault python:3.6-slim "python --version"
    ```

2.  **Run a Node.js script with an older runtime:**
    ```bash
    # Assuming you have an 'index.js' and 'package.json' in your current directory
    ./nightly-version-vault node:12-alpine "npm install && node index.js"
    ```

3.  **Compile C code with a specific GCC version:**
    ```bash
    # Assuming you have 'main.c' in your current directory
    ./nightly-version-vault gcc:7 "gcc main.c -o myapp && ./myapp"
    ```

4.  **Explore an old Ubuntu environment:**
    ```bash
    ./nightly-version-vault ubuntu:18.04 "ls -la / && cat /etc/os-release"
    ```

## How It Works
The `nightly-version-vault` script leverages Docker to create a temporary container. It performs the following steps:
1.  Pulls the specified Docker image (if not already present locally).
2.  Mounts your current working directory into `/app` inside the container.
3.  Sets the working directory inside the container to `/app`.
4.  Executes your provided command using `bash -c` within this isolated environment.
5.  Automatically removes the container upon exit, leaving no trace on your system.

This ensures that your local development environment remains pristine, while you can freely experiment with different software versions.
