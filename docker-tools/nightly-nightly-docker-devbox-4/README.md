# Nightly Docker DevBox

A whimsical-yet-useful containerized development environment that provides customizable language stacks with persistent data volumes. Perfect for developers who want a clean, isolated workspace without polluting their host system.

## Features

- **Multi-language support**: Python, Rust, Go, Node.js, Java, and C++ development environments
- **Persistent volumes**: Your code and data persist between container restarts
- **Customizable stacks**: Mix and match language tools in a single container
- **Quick setup**: One command to get a fully functional dev environment
- **Resource efficient**: Only installs what you need

## Quick Start

### Prerequisites

- Docker installed on your system
- Basic familiarity with Docker commands

### Usage

1. **Build the base image**:

```bash
# Build the multi-stage base image
./scripts/build.sh
```

2. **Create a development environment**:

```bash
# Create a Python development environment
./scripts/create_devbox.sh python my-python-project

# Create a Rust development environment
./scripts/create_devbox.sh rust my-rust-project

# Create a multi-language environment
./scripts/create_devbox.sh "python,rust,go" my-multi-lang-project
```

3. **Start your development environment**:

```bash
# Start the container
./scripts/start_devbox.sh my-python-project

# Attach to the running container
./scripts/attach_devbox.sh my-python-project
```

4. **Stop and clean up**:

```bash
# Stop the container
./scripts/stop_devbox.sh my-python-project

# Remove the container (keeps volumes)
./scripts/remove_devbox.sh my-python-project

# Clean up everything including volumes
./scripts/cleanup_devbox.sh my-python-project
```

## Language Stacks

### Python Stack
- Python 3.11
- pip, venv, virtualenv
- pytest, black, flake8
- Jupyter Notebook

### Rust Stack
- Rust toolchain (rustc, cargo)
- rustfmt, clippy
- ripgrep, fd-find

### Go Stack
- Go 1.21
- gofmt, go vet
- Delve debugger

### Node.js Stack
- Node.js 18+
- npm, yarn
- ESLint, Prettier

### Java Stack
- OpenJDK 17
- Maven, Gradle
- JUnit

### C++ Stack
- GCC, Clang
- CMake, Make
- gdb, valgrind

## Customization

### Adding New Language Stacks

1. Add a new stage to `Dockerfile`:

```dockerfile
# New Language Stage
FROM base AS newlang
RUN apt-get update && apt-get install -y newlang-tools
```

2. Update `scripts/build.sh` to include the new stage
3. Add the language to `scripts/create_devbox.sh` logic

### Custom Development Environments

Create a custom stack by combining multiple languages:

```bash
# Create a full-stack development environment
./scripts/create_devbox.sh "python,rust,go,nodejs" fullstack-dev
```

## Project Structure

```
├── Dockerfile              # Multi-stage Dockerfile with all language stacks
├── docker-compose.yml    # Docker Compose configuration for easy setup
├── scripts/               # Helper scripts for managing devboxes
│   ├── build.sh          # Build the base Docker image
│   ├── create_devbox.sh  # Create a new development environment
│   ├── start_devbox.sh   # Start a development environment
│   ├── attach_devbox.sh  # Attach to a running container
│   ├── stop_devbox.sh    # Stop a development environment
│   ├── remove_devbox.sh  # Remove a container
│   └── cleanup_devbox.sh # Clean up everything including volumes
├── examples/             # Example projects for each language
│   ├── python-app/       # Sample Python application
│   ├── rust-app/         # Sample Rust application
│   └── go-app/           # Sample Go application
└── README.md
```

## Examples

### Python Example

```bash
# Create and start a Python dev environment
./scripts/create_devbox.sh python python-example
./scripts/start_devbox.sh python-example

# Attach and work
./scripts/attach_devbox.sh python-example

# Inside the container
cd /workspace
python -m venv venv
source venv/bin/activate
pip install -r /examples/python-app/requirements.txt
python /examples/python-app/main.py
```

### Rust Example

```bash
# Create and start a Rust dev environment
./scripts/create_devbox.sh rust rust-example
./scripts/start_devbox.sh rust-example

# Attach and work
./scripts/attach_devbox.sh rust-example

# Inside the container
cd /workspace
cargo new my_rust_project
cd my_rust_project
cargo run
```

## Tips and Tricks

### Persistent Data

Your `/workspace` directory is mounted as a Docker volume, so:
- Your code persists between container restarts
- You can stop and start containers without losing work
- Multiple containers can share the same volume

### Customizing Your Environment

You can customize your development environment by:
1. Creating a `.devboxrc` file in your project directory
2. Adding custom environment variables
3. Installing additional packages via `apt` or language-specific package managers

### Performance Tips

- Use named volumes for better performance than bind mounts
- Limit container resources if needed: `docker run --memory=2g --cpus=2`
- Use `.dockerignore` to exclude unnecessary files from the build context

## Troubleshooting

### Container Won't Start

```bash
# Check if the image was built successfully
docker images | grep nightly-devbox

# Check for any build errors
./scripts/build.sh
```

### Volume Issues

```bash
# List all volumes
docker volume ls

# Remove orphaned volumes
docker volume prune
```

### Permission Issues

If you encounter permission issues with mounted volumes:

```bash
# Set proper permissions
sudo chown -R $USER:$USER /path/to/your/workspace
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

If you encounter issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [examples](#examples)
3. Create an issue with detailed information about your problem

---

**Note**: This is a community-driven project. Contributions and feedback are always welcome!
