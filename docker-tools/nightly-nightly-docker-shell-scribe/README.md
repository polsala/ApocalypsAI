# Nightly Docker Shell Scribe

The ApocalypsAI Nightly Integrator presents the **Nightly Docker Shell Scribe**, a whimsical yet highly practical containerized utility designed to act as a "memory vault" for your project's shell commands. Ever forget that one obscure `docker-compose` command or `kubectl` incantation you used last week? The Scribe remembers!

This tool allows you to record important commands, replay them with a touch of temporal echo, and keep your project's operational history consistent and accessible, even across different development environments.

## Features

*   **Record Commands**: Easily log any shell command with a timestamp.
*   **Replay History**: View your recorded commands, presented with a "temporal whisper" effect.
*   **Clear Vault**: Reset the command history for a fresh start.
*   **Containerized**: Runs in a lightweight Docker container, ensuring portability and minimal host dependencies.

## Usage

### 1. Build the Docker Image

First, navigate to the `nightly-docker-shell-scribe` directory and build the Docker image:

```bash
docker build -t nightly-shell-scribe .
```

### 2. Prepare Your Project Directory

The Scribe needs a place to store its memories. Create a `.scribe` directory in your project root, or choose any other location. This directory will be mounted as a volume to persist your command log.

```bash
mkdir -p my-project/.scribe
```

### 3. Run the Scribe

You'll interact with the Scribe by running its Docker container, mounting your chosen `.scribe` directory.

**Important**: Replace `/path/to/your/my-project/.scribe` with the actual path to your project's `.scribe` directory.

#### Record a Command

To record a command, use the `record` argument followed by the command you want to save.

```bash
docker run --rm -v /path/to/your/my-project/.scribe:/app/vault nightly-shell-scribe record "git commit -m 'Initial commit of the temporal echo chamber'"
docker run --rm -v /path/to/your/my-project/.scribe:/app/vault nightly-shell-scribe record "docker-compose up -d --build"
```

The command will be appended to `my-project/.scribe/commands.log` with a timestamp.

#### Replay Command History

To view all recorded commands, use the `replay` argument. Each command will be presented with a unique "temporal whisper" prefix.

```bash
docker run --rm -v /path/to/your/my-project/.scribe:/app/vault nightly-shell-scribe replay
```

Example output:
```
--- Temporal Echoes from the Vault ---
[Temporal Echo]: [2023-10-27 10:30:00] git commit -m 'Initial commit of the temporal echo chamber'
[Temporal Echo]: [2023-10-27 10:35:15] docker-compose up -d --build
--------------------------------------
```

#### Clear the Command Vault

To clear all recorded commands from the log file:

```bash
docker run --rm -v /path/to/your/my-project/.scribe:/app/vault nightly-shell-scribe clear
```

This will empty `my-project/.scribe/commands.log`.

## Development

The `scribe.sh` script expects a mounted volume at `/app/vault` where it will store `commands.log`. Ensure your volume mount points to this internal path.
