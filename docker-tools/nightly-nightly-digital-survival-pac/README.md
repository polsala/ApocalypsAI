# Nightly Digital Survival Pack

A containerized digital survival kit providing essential CLI tools for post-apocalyptic system administration and data wrangling, ensuring you always have your favorite utilities, even when the network is a mere whisper.

## Features

*   **Portable:** Run anywhere Docker is available.
*   **Self-contained:** All tools are bundled within the image.
*   **Essential Toolkit:** Includes `bash`, `curl`, `jq`, `grep`, `awk`, `sed`, `git`, `htop`, `nmap`, `ssh-client`, `rsync`, `vim`.
*   **Consistent Environment:** Avoids "it works on my machine" issues in the wasteland.

## Usage

### Build the Docker Image

Navigate to the `nightly-digital-survival-pack` directory and run:

```bash
docker build -t nightly-digital-survival-pack .
```

### Run a Command within the Pack

To execute a specific command (e.g., check `jq` version):

```bash
docker run --rm nightly-digital-survival-pack jq --version
```

### Enter an Interactive Shell

To drop into a `bash` shell inside the container:

```bash
docker run -it --rm nightly-digital-survival-pack
```

### Mount Local Files (e.g., for editing or processing)

To work on local files, mount a volume:

```bash
docker run -it --rm -v "$(pwd):/data" nightly-digital-survival-pack bash
# Inside the container, your current directory will be at /data
ls /data
vim /data/my_survival_plan.txt
```

## Included Tools

*   `bash`: The ubiquitous shell.
*   `curl`: Transfer data with URLs.
*   `jq`: Lightweight and flexible command-line JSON processor.
*   `grep`, `awk`, `sed`: Powerful text processing utilities.
*   `git`: Distributed version control system (for your survival manifestos).
*   `htop`: Interactive process viewer.
*   `nmap`: Network exploration tool and security / port scanner.
*   `ssh-client`: Secure Shell client (for connecting to that one remaining server).
*   `rsync`: Fast, versatile, remote (and local) file-copying tool.
*   `vim`: Highly configurable text editor.

## Development & Testing

See `tests/test_pack.sh` for how to verify the utility.
