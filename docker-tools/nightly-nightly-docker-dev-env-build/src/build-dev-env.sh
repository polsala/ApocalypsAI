#!/bin/bash

# Nightly Docker Dev Environment Builder
# A whimsical-yet-useful tool for creating containerized development environments

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DEFAULT_STACK="python"
DEFAULT_NAME="dev-env"
DEFAULT_PORT="8080"

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
STACKS_DIR="$SCRIPT_DIR/stacks"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Create a containerized development environment with customizable language stacks.

OPTIONS:
    -s, --stack STACK     Language stack to use (default: $DEFAULT_STACK)
    -n, --name NAME       Project name (default: $DEFAULT_NAME)
    -p, --port PORT       Port to expose (default: $DEFAULT_PORT)
    -c, --config FILE     Custom configuration file
    -h, --help           Show this help message

AVAILABLE STACKS:
$(list_available_stacks)

EXAMPLES:
    $0 --stack python --name my-project
    $0 -s rust -n rust-app -p 3000
    $0 --stack custom --config .dev-env.yml

EOF
}

list_available_stacks() {
    if [[ -d "$STACKS_DIR" ]]; then
        for stack_dir in "$STACKS_DIR"/*/; do
            if [[ -d "$stack_dir" ]]; then
                stack_name=$(basename "$stack_dir")
                echo "    - $stack_name"
            fi
        done
    else
        echo "    - python (default)"
        echo "    - rust"
        echo "    - go"
        echo "    - node"
        echo "    - java"
    fi
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        log_info "Please install Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        log_info "Please start Docker daemon"
        exit 1
    fi
}

create_project_structure() {
    local project_name="$1"
    local stack="$2"

    log_info "Creating project structure for '$project_name' with stack '$stack'"

    # Create project directory
    mkdir -p "$project_name"
    cd "$project_name"

    # Copy common templates
    if [[ -d "$TEMPLATES_DIR" ]]; then
        cp -r "$TEMPLATES_DIR"/* . 2>/dev/null || true
    fi

    # Copy stack-specific files
    if [[ -d "$STACKS_DIR/$stack" ]]; then
        cp -r "$STACKS_DIR/$stack"/* . 2>/dev/null || true
    fi

    # Create .devcontainer if VS Code integration is available
    if [[ -f ".devcontainer-template.json" ]]; then
        sed "s/{{STACK_NAME}}/$stack/g" ".devcontainer-template.json" > ".devcontainer.json"
        rm ".devcontainer-template.json"
    fi

    log_success "Project structure created successfully"
}

generate_dockerfile() {
    local stack="$1"
    local project_name="$2"

    log_info "Generating Dockerfile for stack '$stack'"

    # Use stack-specific Dockerfile if available
    if [[ -f "$stack/Dockerfile" ]]; then
        cp "$stack/Dockerfile" .
        log_success "Using stack-specific Dockerfile"
    else
        # Generate generic Dockerfile
        cat > Dockerfile << EOF
# Generated Dockerfile for $stack development environment
FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install basic tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    vim \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Expose default port
EXPOSE $DEFAULT_PORT

# Default command
CMD ["/bin/bash"]
EOF
        log_success "Generated generic Dockerfile"
    fi
}

generate_docker_compose() {
    local project_name="$1"
    local port="$2"

    log_info "Generating docker-compose.yml"

    cat > docker-compose.yml << EOF
version: '3.8'

services:
  app:
    build: .
    ports:
      - "$port:$port"
    volumes:
      - .:/app
      - /app/node_modules
    working_dir: /app
    command: tail -f /dev/null
    stdin_open: true
    tty: true
EOF

    log_success "Generated docker-compose.yml"
}

generate_vscode_config() {
    local stack="$1"

    log_info "Generating VS Code dev container configuration"

    mkdir -p .devcontainer

    cat > .devcontainer/devcontainer.json << EOF
{
    "name": "$stack Development Environment",
    "dockerComposeFile": "docker-compose.yml",
    "service": "app",
    "workspaceFolder": "/app",
    "features": {
        "ghcr.io/devcontainers/features/common-utils:2": {
            "installZsh": true,
            "configureZshAsDefaultShell": true,
            "installOhMyZsh": true,
            "upgradePackages": true
        }
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-vscode.vscode-json",
                "redhat.vscode-yaml",
                "ms-vscode.vscode-typescript-next"
            ]
        }
    },
    "forwardPorts": [$DEFAULT_PORT],
    "postCreateCommand": "echo 'Development environment ready!'"
}
EOF

    log_success "Generated VS Code dev container configuration"
}

setup_stack() {
    local stack="$1"

    log_info "Setting up stack '$stack'"

    # Run stack-specific setup if available
    if [[ -f "$stack/setup.sh" ]]; then
        chmod +x "$stack/setup.sh"
        bash "$stack/setup.sh"
        log_success "Stack setup completed"
    else
        log_warning "No setup script found for stack '$stack'"
    fi
}

main() {
    local stack="$DEFAULT_STACK"
    local name="$DEFAULT_NAME"
    local port="$DEFAULT_PORT"
    local config_file=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -s|--stack)
                stack="$2"
                shift 2
                ;;
            -n|--name)
                name="$2"
                shift 2
                ;;
            -p|--port)
                port="$2"
                shift 2
                ;;
            -c|--config)
                config_file="$2"
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # Validate inputs
    if [[ -z "$stack" ]]; then
        log_error "Stack cannot be empty"
        exit 1
    fi

    if [[ -z "$name" ]]; then
        log_error "Project name cannot be empty"
        exit 1
    fi

    # Check prerequisites
    check_docker

    # Create project
    create_project_structure "$name" "$stack"
    generate_dockerfile "$stack" "$name"
    generate_docker_compose "$name" "$port"
    generate_vscode_config "$stack"
    setup_stack "$stack"

    # Final instructions
    log_success "Development environment '$name' created successfully!"
    echo
    log_info "Next steps:"
    echo "  cd $name"
    echo "  docker compose up -d"
    echo "  # Open in VS Code and click 'Reopen in Container'"
    echo
    log_info "To stop the environment:"
    echo "  docker compose down"
}

# Run main function with all arguments
main "$@"
