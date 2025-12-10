# Nightly Docker DevBox

A containerized development environment pre-configured with essential tools for ApocalypsAI contributors. Perfect for consistent development across different machines.

## Features

- Pre-installed development tools (git, curl, jq, make, etc.)
- Python 3.11 with common packages
- Rust toolchain
- Go environment
- Node.js and npm
- Docker-in-Docker support
- VS Code Remote Container support

## Quick Start

### Prerequisites

- Docker installed on your machine
- Optional: VS Code with Remote Containers extension

### Using the DevBox

1. Clone this repository
2. Navigate to the nightly-docker-devbox directory
3. Run the container:

```bash
# Start the development environment
docker compose up -d

# Or run interactively
docker compose run --rm devbox

# Attach to running container
docker compose exec devbox bash
```

### VS Code Integration

1. Open VS Code in this directory
2. When prompted, select "Reopen in Container"
3. Start coding!

### Available Tools

The container includes:

- **Python 3.11**: pip, pytest, requests, rich
- **Rust**: cargo, rustfmt, clippy
- **Go 1.21**: gofmt, go vet
- **Node.js 18**: npm, npx
- **Development tools**: git, curl, jq, make, vim, tmux
- **Docker CLI**: connect to host Docker daemon

## Customization

Edit the Dockerfile or docker-compose.yml to add your preferred tools and configurations.

## License

MIT
