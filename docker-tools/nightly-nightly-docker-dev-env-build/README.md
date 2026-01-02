# Nightly Docker Dev Environment Builder

A whimsical-yet-useful tool for creating containerized development environments with customizable language stacks and VS Code integration.

## Features

- 🐳 **Containerized Development**: Spin up isolated dev environments in Docker containers
- 🎨 **Multi-Language Support**: Pre-configured stacks for Python, Rust, Go, Node.js, and more
- 🔧 **VS Code Integration**: Automatic VS Code dev container configuration
- 📦 **Customizable**: Easy to extend with new language stacks
- 🚀 **Quick Setup**: One command to get a fully configured dev environment

## Quick Start

### Prerequisites

- Docker installed and running
- VS Code with Remote - Containers extension (optional but recommended)

### Usage

1. **Generate a dev environment**:

```bash
./build-dev-env.sh --stack python --name my-python-project
```

2. **Start the environment**:

```bash
cd my-python-project && docker compose up -d
```

3. **Connect with VS Code**:

Open the project folder in VS Code and click "Reopen in Container" when prompted.

### Available Stacks

- `python` - Python 3.11 with pip, virtualenv, and common dev tools
- `rust` - Rust with cargo, rustfmt, and clippy
- `go` - Go with gofmt, golangci-lint, and delve
- `node` - Node.js with npm, yarn, and common JavaScript tools
- `java` - Java with Maven, Gradle, and common JVM tools
- `custom` - Build your own stack with the configuration file

### Configuration

Create a `.dev-env.yml` file in your project root to customize your environment:

```yaml
stack: python
packages:
  - numpy
  - pandas
  - flask
ports:
  - "8080:8080"
  - "3000:3000"
volumes:
  - ./data:/app/data
env:
  DEBUG: true
  LOG_LEVEL: info
```

## Advanced Usage

### Custom Language Stacks

Add new language stacks by creating a directory in `stacks/` with:

- `Dockerfile` - Base container configuration
- `setup.sh` - Post-installation setup script
- `README.md` - Documentation for the stack

### Multi-Service Environments

For complex projects, use the `docker-compose.yml` template to define multiple services:

```yaml
services:
  app:
    build: .
    ports:
      - "8080:8080"
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

## Contributing

1. Fork the repository
2. Create a new stack in `stacks/your-stack-name/`
3. Add tests in `tests/`
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue or join our Discord community.

---

*Built with ❤️ by the ApocalypsAI community*
