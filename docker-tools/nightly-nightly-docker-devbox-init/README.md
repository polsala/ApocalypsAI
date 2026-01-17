# nightly-docker-devbox-init

A lightweight utility to scaffold Docker-based development environments with pre-configured toolchains.

## Features

- Generate isolated dev containers with language presets (Python, Node.js, Go, Rust)
- Versioned base images for reproducibility
- Built-in volume mounting and port forwarding
- Headless-ready for CI/CD or remote dev

## Usage

```bash
# Initialize a Python 3.11 devbox
./init-devbox.sh python

# Initialize a Node.js 18 devbox
./init-devbox.sh node

# Initialize a Go 1.21 devbox
./init-devbox.sh go

# Initialize a Rust devbox
./init-devbox.sh rust
```

Each command generates a `Dockerfile`, `docker-compose.yml`, and `.devbox/` metadata.

## Requirements

- Docker
- Docker Compose

## Testing

Run `./test.sh` to validate all presets build and run correctly.
