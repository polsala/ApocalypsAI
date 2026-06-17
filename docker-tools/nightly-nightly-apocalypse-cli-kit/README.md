# Nightly Apocalypse CLI Kit

## Summary

The `nightly-apocalypse-cli-kit` is a whimsical-yet-useful containerized toolkit designed to equip the community with a consistent set of essential command-line tools for navigating the digital detritus of a post-apocalyptic world. Whether you're parsing salvaged data logs, checking for faint network signals, or monitoring scavenged server vitals, this kit ensures you have the right tools at your fingertips, isolated and ready.

## Whimsical Use Cases

*   **Salvaged Data Forensics**: Use `jq` to parse corrupted JSON logs from ancient data drives, trying to piece together pre-apocalypse memes.
*   **Signal Scavenging**: `curl` the desolate airwaves for any lingering HTTP responses from forgotten servers, hoping for a sign of intelligent life (or just a working API).
*   **Wasteland Log Analysis**: `grep` through vast, unindexed text files found in abandoned data centers, searching for keywords like "food," "water," or "working power outlet."
*   **Quick Command Reminders**: If your memory banks are failing due to radiation exposure, `tldr` provides simplified man pages for common commands.
*   **Scavenged Server Monitoring**: Keep an eye on the vital signs of your jury-rigged server with `htop`, ensuring it doesn't overheat while mining for crypto-scraps.
*   **Config File Deciphering**: Use `bat` to view and syntax-highlight ancient configuration files, trying to understand how the old world's systems worked.
*   **Navigating Forgotten Directories**: `fzf` helps you fuzzy-find your way through vast, unorganized file systems on recovered storage devices.

## Included Tools

The kit comes pre-loaded with the following essential utilities:

*   `jq`: Lightweight and flexible command-line JSON processor.
*   `curl`: Tool for transferring data with URLs, essential for network diagnostics.
*   `grep`: Powerful text search utility.
*   `tldr`: Simplified and community-driven man pages.
*   `htop`: Interactive process viewer.
*   `bat`: A `cat` clone with wings (syntax highlighting, Git integration, etc.).
*   `fzf`: A command-line fuzzy finder.

## How to Use

### 1. Build the Docker Image

Navigate to the `nightly-apocalypse-cli-kit` directory and build the Docker image:

```bash
docker build -t apocalypsai-cli-kit .
```

### 2. Run the Kit

#### Interactive Shell

To drop into an interactive `bash` shell within the container, where all tools are available:

```bash
docker run -it apocalypsai-cli-kit
```

#### Execute a Specific Command

You can also execute a specific command directly:

```bash
docker run --rm apocalypsai-cli-kit jq --version
docker run --rm apocalypsai-cli-kit curl https://example.com
```

#### List Available Tools

The `entrypoint.sh` script includes a special command to list the pre-installed tools and their whimsical purposes:

```bash
docker run --rm apocalypsai-cli-kit list-tools
```

## Development & Testing

To ensure the kit is always ready for the next societal collapse, automated tests are provided.

```bash
./tests/test_kit.sh
```

This script will build the Docker image, run various checks to ensure the tools are present and the entrypoint functions correctly, and then clean up the test image.
