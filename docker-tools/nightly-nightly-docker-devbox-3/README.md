# Nightly Docker DevBox

A whimsical-yet-useful Docker-based development environment generator with interactive TTY and health monitoring.

## Features

- 🚀 Spin up a complete development environment in seconds
- 🎨 Whimsical ASCII art welcome screen
- 📊 Real-time health monitoring with Prometheus metrics
- 🐛 Interactive debugging with custom commands
- 🧹 Automatic cleanup and resource management
- 🎯 Pre-configured for multiple languages (Python, Node.js, Rust, Go)

## Quick Start

```bash
# Clone and run
git clone <repo>
cd nightly-docker-devbox

# Build the devbox
./scripts/build.sh

# Start your development environment
./scripts/run.sh python

# Access the interactive console
./scripts/console.sh

# View health metrics
./scripts/metrics.sh

# Clean up
./scripts/cleanup.sh
```

## Supported Languages

- `python` - Python 3.11 with common dev tools
- `node` - Node.js 20 with npm and yarn
- `rust` - Rust with cargo and rustfmt
- `go` - Go 1.21 with standard tools

## Architecture

```
+-------------------+     +-------------------+
|   DevBox CLI      |     |   Docker Engine   |
|   (scripts/)      |---->|   (containers)    |
+-------------------+     +-------------------+
                                |
                                v
                    +-------------------+
                    |   Health Monitor  |
                    |   (Prometheus)    |
                    +-------------------+
```

## Development

### Adding New Language Profiles

1. Create a new Dockerfile in `dockerfiles/Dockerfile.<language>`
2. Add the language to `scripts/run.sh`
3. Update `README.md` with the new option

### Customizing the Welcome Screen

Edit `assets/welcome.txt` with your ASCII art masterpiece.

## Testing

```bash
# Run all tests
./scripts/test.sh

# Run specific test suite
./scripts/test.sh unit
./scripts/test.sh integration
```

## License

MIT - because even apocalyptic AIs need to share their toys!
