# Nightly Chrono-Container Courier (NCCC)

## Summary
The Nightly Chrono-Container Courier (NCCC) is a whimsical-yet-useful Docker-based utility designed to transport your commands back in time (or to any specified environment) within an isolated container. It allows you to run scripts or commands against specific historical or custom Docker images, capturing their output for reproducible testing, debugging legacy systems, or simply satisfying your curiosity about how things used to run.

## How it Works
NCCC takes a `config.json` file specifying a Docker image and a list of commands. It then:
1.  Pulls the specified Docker image (e.g., `ubuntu:18.04`, `node:14`).
2.  Spins up a temporary container using that image.
3.  Executes your defined commands sequentially within the container.
4.  Captures all standard output, standard error, and the final exit code.
5.  Writes the captured output to a designated log file on your host machine.

This allows you to simulate specific environments without altering your host system, making it perfect for testing backward compatibility, debugging dependency conflicts, or verifying "it worked on my machine last year" scenarios.

## Prerequisites
*   **Docker**: The Docker daemon must be running and accessible on your system.
*   **`jq`**: A lightweight and flexible command-line JSON processor, used for parsing the configuration file. Install it via your package manager (e.g., `sudo apt-get install jq` on Debian/Ubuntu, `brew install jq` on macOS).

## Usage
1.  **Create a `config.json` file** in the directory where you'll run the courier, or specify its path.
    See `src/config_template.json` for an example.

2.  **Run the `chrono_courier.sh` script**:
    ```bash
    ./src/chrono_courier.sh [path/to/your/config.json]
    ```
    If no path is provided, it defaults to `config.json` in the current directory.

## Configuration (`config.json`)
The `config.json` file defines the environment and commands for the courier. Here's an example:

```json
{
  "image": "ubuntu:20.04",
  "commands": [
    "apt update && apt install -y curl -qq > /dev/null",
    "curl -s https://www.example.com",
    "echo 'Hello from the past (Ubuntu 20.04)!'"
  ],
  "output_file": "chrono_courier_output.log",
  "mount_path": "/app"
}
```

*   `image` (string, required): The Docker image to use as the base for your time capsule (e.g., `python:3.8-slim`, `node:14-alpine`, `debian:buster`).
*   `commands` (array of strings, required): A list of shell commands to execute sequentially inside the container. Each command will be run in a single shell session.
*   `output_file` (string, optional): The name of the file where the container's stdout and stderr will be saved. Defaults to `chrono_courier_results.log`.
*   `mount_path` (string, optional): The path inside the container where the current host directory will be mounted. Defaults to `/app`. This is useful if your commands need to access files from your host.

## Example
Let's say you want to test a script (`my_old_script.py`) that only works with Python 3.6.

**`config.json`:**
```json
{
  "image": "python:3.6-slim",
  "commands": [
    "pip install requests",
    "python /app/my_old_script.py"
  ],
  "output_file": "python_3_6_test.log",
  "mount_path": "/app"
}
```

**`my_old_script.py`:**
```python
import sys
import requests

print(f"Running on Python {sys.version.split()[0]}")
try:
    response = requests.get("http://httpbin.org/get")
    print(f"Request successful: {response.status_code}")
except Exception as e:
    print(f"Request failed: {e}")
```

Run the courier:
```bash
./src/chrono_courier.sh
```

After execution, `python_3_6_test.log` will contain the output from your script running in the Python 3.6 environment.
