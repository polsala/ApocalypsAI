# Nightly Docker DevBox

A whimsical-yet-useful containerized development environment generator with interactive terminal UI. Spin up pre-configured development boxes for any language or framework with a single command!

## Features

- 🚀 **One-command setup**: Generate and launch development environments in seconds
- 🎨 **Interactive UI**: Choose your stack with a beautiful terminal interface
- 🐳 **Containerized**: Everything runs in Docker for consistency and isolation
- 📦 **Pre-configured**: Ready-to-code environments with common tools and dependencies
- 🎯 **Customizable**: Easy to extend with new templates and configurations
- 🧪 **Testing included**: Automated tests ensure reliability

## Quick Start

```bash
# Clone the repository
git clone <repo-url>
cd docker-tools/nightly-docker-devbox

# Run the interactive setup
./devbox.sh

# Or use the CLI directly
./devbox.sh --template python --name my-python-project
```

## Supported Templates

- **Python**: Python 3.11 with pip, venv, and common dev tools
- **Node.js**: Node.js 20 with npm, yarn, and essential packages
- **Rust**: Rust toolchain with cargo and common crates
- **Go**: Go 1.21 with essential tools and modules
- **Java**: OpenJDK 17 with Maven and Gradle
- **Ruby**: Ruby 3.2 with Bundler and Rails
- **PHP**: PHP 8.2 with Composer and Xdebug
- **Custom**: Load your own template configuration

## CLI Usage

```bash
# Show help
./devbox.sh --help

# List available templates
./devbox.sh --list-templates

# Create a new development environment
./devbox.sh --template <template-name> --name <project-name>

# Start an existing environment
./devbox.sh --start --name <project-name>

# Stop an environment
./devbox.sh --stop --name <project-name>

# Remove an environment
./devbox.sh --remove --name <project-name>

# Execute a command in a running environment
./devbox.sh --exec --name <project-name> --command "npm run dev"
```

## Interactive Mode

Run `./devbox.sh` without arguments to launch the interactive terminal UI:

1. **Select Template**: Choose from available development environments
2. **Configure Project**: Set project name, ports, and customizations
3. **Review Settings**: Preview your configuration before creation
4. **Launch**: Start your development environment

## Custom Templates

Create your own development environment templates by adding JSON configuration files to the `templates/` directory:

```json
{
  "name": "my-custom-stack",
  "description": "My custom development stack",
  "dockerfile": "Dockerfile.custom",
  "ports": [3000, 8080],
  "volumes": ["./src:/app/src"],
  "environment": {
    "NODE_ENV": "development"
  },
  "startup_command": "npm run dev",
  "dependencies": ["nodejs", "npm"]
}
```

## Project Structure

```
docker-tools/nightly-docker-devbox/
├── README.md              # This file
├── devbox.sh             # Main CLI script
├── templates/            # Development environment templates
│   ├── python.json     # Python development template
│   ├── nodejs.json     # Node.js development template
│   ├── rust.json       # Rust development template
│   └── go.json         # Go development template
├── Dockerfile          # Base Dockerfile
├── docker-compose.yml  # Docker Compose configuration
├── tests/              # Automated tests
│   ├── test_devbox.sh  # Shell script tests
│   └── test_templates.sh # Template validation tests
└── scripts/            # Helper scripts
    ├── generate_dockerfile.sh
    └── validate_template.sh
```

## Requirements

- Docker 20.10+
- Docker Compose 2.0+
- Bash 4.0+
- jq (for JSON processing)

## Installation

1. Clone the repository
2. Make the scripts executable:
   ```bash
   chmod +x devbox.sh
   chmod +x scripts/*.sh
   ```
3. Install jq if not already available:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install jq
   
   # macOS
   brew install jq
   
   # CentOS/RHEL
   sudo yum install jq
   ```

## Development

### Adding New Templates

1. Create a new JSON template in `templates/`
2. Add the corresponding Dockerfile
3. Update the template registry in `devbox.sh`
4. Add tests in `tests/`
5. Run the test suite: `./tests/test_devbox.sh`

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-template`
3. Make your changes
4. Add tests for your changes
5. Run the test suite: `./tests/test_devbox.sh`
6. Commit your changes: `git commit -am 'Add new development template'`
7. Push to the branch: `git push origin feature/new-template`
8. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

If you encounter issues or have suggestions:

1. Check the existing issues
2. Create a new issue with:
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Docker version, etc.)

## Security

- All containers run with minimal privileges
- No secrets are stored in the repository
- Templates are validated before use
- Regular security updates for base images

## Performance

- Optimized Docker images with multi-stage builds
- Efficient volume mounting for development
- Resource limits can be configured per template
- Fast startup times with pre-built layers

## Examples

### Python Development

```bash
./devbox.sh --template python --name my-python-app
```

This creates a Python 3.11 environment with:
- Virtual environment setup
- Common development tools (pytest, black, flake8)
- Port 8000 exposed for web applications
- Volume mapping for live code changes

### Node.js Development

```bash
./devbox.sh --template nodejs --name my-node-app
```

This creates a Node.js 20 environment with:
- npm and yarn available
- Common development dependencies
- Port 3000 exposed for development servers
- Hot reload support

### Rust Development

```bash
./devbox.sh --template rust --name my-rust-project
```

This creates a Rust environment with:
- Cargo toolchain
- Common crates pre-installed
- Port 8080 exposed for web services
- Debug and release build support

Enjoy coding in your containerized development paradise! 🚀🐳
