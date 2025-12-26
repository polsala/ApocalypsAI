#!/bin/bash

# Nightly Docker DevBox Creation Script
# Creates a new development environment with specified language stacks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker is not running. Please start Docker daemon."
        exit 1
    fi
}

# Validate language stack
validate_stack() {
    local stack="$1"
    local valid_stacks=("python" "rust" "go" "nodejs" "java" "cpp")
    
    for lang in $(echo "$stack" | tr ',' ' '); do
        if [[ ! " ${valid_stacks[@]} " =~ " ${lang} " ]]; then
            log_error "Invalid language stack: $lang"
            log_info "Valid stacks: ${valid_stacks[*]}"
            exit 1
        fi
    done
}

# Create development environment
create_devbox() {
    local stack="$1"
    local name="$2"
    
    log_info "Creating development environment '$name' with stack: $stack"
    
    # Check if container already exists
    if docker ps -a --format "table {{.Names}}" | grep -q "^${name}$"; then
        log_warn "Container '$name' already exists. Please choose a different name or remove the existing container."
        exit 1
    fi
    
    # Create volume for persistent data
    docker volume create "${name}_workspace" 2>/dev/null || true
    
    # Create container
    docker create \
        --name "$name" \
        --hostname "devbox-$name" \
        --volume "${name}_workspace:/workspace" \
        --volume "$HOME/.ssh:/root/.ssh:ro" \
        --volume "$HOME/.gitconfig:/root/.gitconfig:ro" \
        --env "TERM=xterm-256color" \
        --env "LANG=C.UTF-8" \
        --publish "8888:8888" \
        --interactive \
        --tty \
        nightly-devbox:latest
    
    if [ $? -eq 0 ]; then
        log_info "Successfully created development environment '$name'"
        log_info "Stack: $stack"
        log_info "Workspace volume: ${name}_workspace"
        log_info "To start the environment, run: ./scripts/start_devbox.sh $name"
    else
        log_error "Failed to create development environment '$name'"
        exit 1
    fi
}

# Show usage information
show_usage() {
    echo "Usage: $0 <language_stack> <environment_name>"
    echo ""
    echo "Language stacks (comma-separated):"
    echo "  python  - Python 3.11 with development tools"
    echo "  rust    - Rust toolchain with cargo"
    echo "  go      - Go 1.21 with development tools"
    echo "  nodejs  - Node.js 18+ with npm"
    echo "  java    - OpenJDK 17 with Maven/Gradle"
    echo "  cpp     - GCC, Clang, and debugging tools"
    echo ""
    echo "Examples:"
    echo "  $0 python my-python-project"
    echo "  $0 "python,rust,go" fullstack-dev"
    echo "  $0 nodejs web-app"
}

# Main execution
main() {
    if [ $# -ne 2 ]; then
        log_error "Invalid number of arguments"
        show_usage
        exit 1
    fi
    
    local stack="$1"
    local name="$2"
    
    log_info "Starting Nightly Docker DevBox creation process"
    
    check_docker
    validate_stack "$stack"
    create_devbox "$stack" "$name"
}

# Run main function
main "$@"
