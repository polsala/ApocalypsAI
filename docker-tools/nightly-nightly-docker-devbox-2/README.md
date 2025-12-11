# Nightly Docker DevBox

A containerized development environment pre-configured with essential tools for ApocalypsAI contributors.

## Features

- Pre-installed development tools (git, curl, jq, make)
- Python 3.11 with common packages
- Rust toolchain
- Node.js LTS
- Docker-in-Docker support
- VS Code Remote Container support

## Quick Start

### Using Docker

```bash
# Build the image
docker build -t nightly-devbox .

# Run with VS Code Remote Container support
docker run -it --rm \
  --name nightly-devbox \
  -v "$(pwd):/workspace" \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 2222:22 \
  nightly-devbox

# Or run with VS Code Remote Container (recommended)
code --folder-uri vscode-remote://attached-container+nightly-devbox/workspace
```

### Using Docker Compose

```bash
# Start the development environment
docker-compose up -d

# Attach VS Code to the container
code --folder-uri vscode-remote://attached-container+nightly-devbox/workspace

# Stop when done
docker-compose down
```

### Using VS Code Remote Containers

1. Install the "Remote - Containers" extension
2. Open this folder in VS Code
3. Press `Ctrl+Shift+P` and run "Remote-Containers: Reopen in Container"
4. The container will build automatically with all tools pre-installed

## Included Tools

### Development Tools
- git 2.40+
- curl 8.0+
- jq 1.6+
- make 4.3+
- wget 1.21+
- vim, nano

### Python Stack
- Python 3.11
- pip, venv
- requests, pyyaml, rich
- pytest, black, flake8

### Rust Toolchain
- Rust 1.70+
- cargo
- rustfmt
- clippy

### Node.js Stack
- Node.js 18+
- npm, npx
- typescript, ts-node
- eslint, prettier

### Docker-in-Docker
- Docker CLI
- Docker daemon (for building images inside container)

## Customization

Edit the `Dockerfile` to add your preferred tools or modify the environment.

## Security Notes

- This container runs with Docker-in-Docker support for convenience
- Do not expose the Docker socket in production environments
- The container runs as root by default for tool installation

## License

MIT - feel free to modify and share!
