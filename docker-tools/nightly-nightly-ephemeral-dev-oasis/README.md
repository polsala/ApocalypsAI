# Nightly Ephemeral Dev Oasis

## Summary
`nightly-ephemeral-dev-oasis` is a whimsical-yet-useful utility designed to provide a clean, isolated, and ephemeral development environment for focused tasks. Think of it as a temporary, self-contained "comfort zone" for your coding needs. It leverages Docker and Docker Compose to quickly spin up a pre-configured shell environment, allowing you to work without polluting your host system, and then tear it down completely.

## Features
- **Ephemeral:** Easily create and destroy isolated development environments.
- **Pre-configured:** Comes with a basic Alpine Linux image, `bash`, `git`, `vim`, `curl`, and `openssh-client` pre-installed.
- **Isolated:** Your host system remains clean, and dependencies are contained within the Docker environment.
- **Simple Interface:** A single `oasis.sh` script manages the lifecycle.
- **Work Persistence (Optional):** Mounts a local `work` directory into the container for easy file sharing and persistence across sessions (if you don't destroy the `work` directory).

## Usage

### Prerequisites
- Docker and Docker Compose installed on your system.

### Setup
1. Navigate to the `nightly-ephemeral-dev-oasis` directory.
2. The `src/` directory contains:
   - `oasis.sh`: The main script.
   - `Dockerfile`: Defines the base image for your oasis.
   - `docker-compose.yml`: Defines the Docker Compose service.

### Commands

#### `create` - Spin up your Oasis
This command builds the Docker image and starts the `oasis-shell` service in detached mode.

```bash
./src/oasis.sh create
```

Upon successful creation, a local directory `src/work` will be created (if it doesn't exist) and mounted into the container at `/app/work`. You can place your project files here.

#### `enter` - Step into your Oasis
This command attaches you to the running `oasis-shell` container, giving you a `bash` prompt inside the isolated environment.

```bash
./src/oasis.sh enter
```

To exit the container without stopping it, type `exit` or press `Ctrl+D`.

#### `destroy` - Dismantle your Oasis
This command stops and removes the `oasis-shell` container, its network, and any anonymous volumes. It leaves the `src/work` directory intact on your host, so your files are safe.

```bash
./src/oasis.sh destroy
```

#### `list` - See active Oases
This command lists the status of the `nightly-oasis-shell` container.

```bash
./src/oasis.sh list
```

## Customization
You can modify `src/Dockerfile` to include additional tools, languages, or dependencies needed for your specific tasks. Similarly, `src/docker-compose.yml` can be adjusted to add more services, expose ports, or configure volumes differently.

## Example Workflow
1. `cd nightly-ephemeral-dev-oasis`
2. `./src/oasis.sh create`
3. `./src/oasis.sh enter`
4. (Inside container) `cd /app/work`
5. (Inside container) `git clone my-project.git .`
6. (Inside container) Work on your project.
7. (Inside container) `exit`
8. `./src/oasis.sh destroy` (when done with the environment)

Your work in `src/work` will persist on your host machine.
