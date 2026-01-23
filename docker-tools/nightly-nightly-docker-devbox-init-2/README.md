# nightly-docker-devbox-init

A utility to scaffold Docker-based development environments for various languages.

## Features

- One-command setup for dev containers
- Language templates: Python, Node.js, Go, Rust
- Auto-generated `Dockerfile` and `docker-compose.yml`

## Usage

```bash
./devbox-init.sh python my-python-project
```

This creates a folder `my-python-project` with Docker setup for Python dev.

## Supported Languages

- `python`
- `node`
- `go`
- `rust`

## License

MIT
