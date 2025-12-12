#!/bin/bash

# Nightly Docker DevBox - Build Script
# Generates a whimsical-yet-useful Docker-based development environment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    log_success "Docker is available"
}

create_directories() {
    log_info "Creating directory structure..."
    mkdir -p "$ROOT_DIR/dockerfiles"
    mkdir -p "$ROOT_DIR/assets"
    mkdir -p "$ROOT_DIR/tests"
    mkdir -p "$ROOT_DIR/scripts"
    log_success "Directory structure created"
}

create_welcome_art() {
    log_info "Creating whimsical welcome art..."
    cat > "$ROOT_DIR/assets/welcome.txt" << 'EOF'
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  ██████╗ ██████╗ ██╗███╗   ██╗███████╗██╗   ██╗███████╗██████╗             ║
║  ██╔══██╗██╔══██╗██║████╗  ██║██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗            ║
║  ██████╔╝██████╔╝██║██╔██╗ ██║█████╗   ╚████╔╝ █████╗  ██████╔╝            ║
║  ██╔═══╝ ██╔══██╗██║██║╚██╗██║██╔══╝    ╚██╔╝  ██╔══╝  ██╔══██╗            ║
║  ██║     ██████╔╝██║██║ ╚████║███████╗   ██║   ███████╗██║  ██║            ║
║  ╚═╝     ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝            ║
║                                                                              ║
║  Welcome to Nightly Docker DevBox!                                          ║
║  Your whimsical-yet-useful development environment awaits...                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
    log_success "Welcome art created"
}

create_dockerfile_python() {
    log_info "Creating Python Dockerfile..."
    cat > "$ROOT_DIR/dockerfiles/Dockerfile.python" << 'EOF'
# Nightly Docker DevBox - Python Environment
# A whimsical-yet-useful development environment

FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Force Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --no-cache-dir \
    pipenv \
    poetry \
    black \
    flake8 \
    pytest \
    mypy \
    ipython \
    jupyter

# Copy requirements if they exist
COPY requirements.txt* . 2>/dev/null || echo "No requirements.txt found"
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || echo "No requirements to install"

# Create a non-root user
RUN useradd --create-home --shell /bin/bash devuser
RUN chown -R devuser:devuser /app
USER devuser

# Add /home/devuser/.local/bin to PATH
ENV PATH=/home/devuser/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["/bin/bash"]
EOF
    log_success "Python Dockerfile created"
}

create_dockerfile_node() {
    log_info "Creating Node.js Dockerfile..."
    cat > "$ROOT_DIR/dockerfiles/Dockerfile.node" << 'EOF'
# Nightly Docker DevBox - Node.js Environment
# A whimsical-yet-useful development environment

FROM node:20-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install global npm packages
RUN npm install -g \
    yarn \
    typescript \
    @angular/cli \
    create-react-app \
    eslint \
    prettier

# Copy package files if they exist
COPY package.json* . 2>/dev/null || echo "No package.json found"
COPY yarn.lock* . 2>/dev/null || echo "No yarn.lock found"
RUN npm install 2>/dev/null || echo "No npm packages to install"
RUN yarn install 2>/dev/null || echo "No yarn packages to install"

# Create a non-root user
RUN useradd --create-home --shell /bin/bash devuser
RUN chown -R devuser:devuser /app
USER devuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Default command
CMD ["/bin/bash"]
EOF
    log_success "Node.js Dockerfile created"
}

create_dockerfile_rust() {
    log_info "Creating Rust Dockerfile..."
    cat > "$ROOT_DIR/dockerfiles/Dockerfile.rust" << 'EOF'
# Nightly Docker DevBox - Rust Environment
# A whimsical-yet-useful development environment

FROM rust:1.70-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Rust tools
RUN rustup component add rustfmt clippy

# Create a non-root user
RUN useradd --create-home --shell /bin/bash devuser
RUN chown -R devuser:devuser /app
USER devuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD cargo --version

# Default command
CMD ["/bin/bash"]
EOF
    log_success "Rust Dockerfile created"
}

create_dockerfile_go() {
    log_info "Creating Go Dockerfile..."
    cat > "$ROOT_DIR/dockerfiles/Dockerfile.go" << 'EOF'
# Nightly Docker DevBox - Go Environment
# A whimsical-yet-useful development environment

FROM golang:1.21-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home --shell /bin/bash devuser
RUN chown -R devuser:devuser /app
USER devuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD go version

# Default command
CMD ["/bin/bash"]
EOF
    log_success "Go Dockerfile created"
}

create_run_script() {
    log_info "Creating run script..."
    cat > "$ROOT_DIR/scripts/run.sh" << 'EOF'
#!/bin/bash

# Nightly Docker DevBox - Run Script
# Start your development environment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

show_usage() {
    echo "Usage: $0 <language> [options]"
    echo ""
    echo "Supported languages:"
    echo "  python    - Python 3.11 with dev tools"
    echo "  node      - Node.js 20 with npm and yarn"
    echo "  rust      - Rust with cargo and rustfmt"
    echo "  go        - Go 1.21 with standard tools"
    echo ""
    echo "Options:"
    echo "  -p, --port PORT    - Map port to host (format: host:container)"
    echo "  -v, --volume PATH  - Mount volume to /app"
    echo "  -n, --name NAME    - Container name"
    echo "  -h, --help         - Show this help"
}

check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
}

build_image() {
    local language=$1
    local image_name="nightly-devbox-$language"
    
    log_info "Building Docker image: $image_name"
    
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.$language" -t "$image_name" "$ROOT_DIR"; then
        log_success "Image built successfully: $image_name"
    else
        log_error "Failed to build image: $image_name"
        exit 1
    fi
}

run_container() {
    local language=$1
    local image_name="nightly-devbox-$language"
    local container_name=${CONTAINER_NAME:-"nightly-devbox-$language-$(date +%s)"}
    local port_mapping=${PORT_MAPPING:-""}
    local volume_mapping=${VOLUME_MAPPING:-""}
    
    # Build image if it doesn't exist
    if ! docker image inspect "$image_name" &> /dev/null; then
        build_image "$language"
    fi
    
    log_info "Starting container: $container_name"
    
    # Prepare Docker run arguments
    local docker_args=(
        "--name" "$container_name"
        "--rm"
        "-it"
        "--health-start-period" "5s"
        "--health-interval" "30s"
        "--health-retries" "3"
        "--health-timeout" "10s"
        "-v" "$ROOT_DIR:/app"
        "-w" "/app"
    )
    
    # Add port mapping if specified
    if [[ -n "$port_mapping" ]]; then
        docker_args+=("-p" "$port_mapping")
    fi
    
    # Add volume mapping if specified
    if [[ -n "$volume_mapping" ]]; then
        docker_args+=("-v" "$volume_mapping")
    fi
    
    # Run the container
    docker run "${docker_args[@]}" "$image_name" /bin/bash -c "
        echo '
╔══════════════════════════════════════════════════════════════════════════════╗'
        echo '║                                                                              ║'
        echo '║  Welcome to Nightly Docker DevBox!                                         ║'
        echo '║                                                                              ║'
        echo '║  Language: $language                                                        ║'
        echo '║  Container: $container_name                                                 ║'
        echo '║  Time: $(date)                                                             ║'
        echo '║                                                                              ║'
        echo '║  Available commands:                                                       ║'
        echo '║    • devbox-help   - Show available commands                                 ║'
        echo '║    • devbox-status - Check container health                                  ║'
        echo '║    • devbox-logs   - View container logs                                     ║'
        echo '║    • devbox-stop   - Stop the container                                      ║'
        echo '║                                                                              ║'
        echo '╚══════════════════════════════════════════════════════════════════════════════╝'
        echo ''
        exec /bin/bash
    "
    
    log_success "Container stopped: $container_name"
}

main() {
    local language=""
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--port)
                PORT_MAPPING="$2"
                shift 2
                ;;
            -v|--volume)
                VOLUME_MAPPING="$2"
                shift 2
                ;;
            -n|--name)
                CONTAINER_NAME="$2"
                shift 2
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                if [[ -z "$language" ]]; then
                    language="$1"
                else
                    log_error "Unknown option: $1"
                    show_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Check if language is specified
    if [[ -z "$language" ]]; then
        log_error "No language specified"
        show_usage
        exit 1
    fi
    
    # Validate language
    case $language in
        python|node|rust|go)
            ;;
        *)
            log_error "Unsupported language: $language"
            show_usage
            exit 1
            ;;
    esac
    
    check_docker
    run_container "$language"
}

main "$@"
EOF
    chmod +x "$ROOT_DIR/scripts/run.sh"
    log_success "Run script created"
}

create_console_script() {
    log_info "Creating console script..."
    cat > "$ROOT_DIR/scripts/console.sh" << 'EOF'
#!/bin/bash

# Nightly Docker DevBox - Console Script
# Access the interactive console

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

show_usage() {
    echo "Usage: $0 [container_name]"
    echo ""
    echo "Access the interactive console of a running Nightly DevBox container."
    echo ""
    echo "If no container name is specified, the script will find the first"
    echo "running Nightly DevBox container."
}

find_container() {
    local container_name=$1
    
    if [[ -n "$container_name" ]]; then
        # Check if specific container exists and is running
        if docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
            echo "$container_name"
            return 0
        else
            log_error "Container not found or not running: $container_name"
            return 1
        fi
    else
        # Find any running Nightly DevBox container
        local containers
        containers=$(docker ps --format "{{.Names}}" | grep "nightly-devbox" | head -1)
        
        if [[ -n "$containers" ]]; then
            echo "$containers"
            return 0
        else
            log_error "No running Nightly DevBox containers found"
            return 1
        fi
    fi
}

main() {
    local container_name=${1:-""}
    
    if [[ "$container_name" == "-h" || "$container_name" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    log_info "Finding container..."
    container_name=$(find_container "$container_name") || exit 1
    
    log_info "Attaching to container: $container_name"
    docker exec -it "$container_name" /bin/bash
}

main "$@"
EOF
    chmod +x "$ROOT_DIR/scripts/console.sh"
    log_success "Console script created"
}

create_metrics_script() {
    log_info "Creating metrics script..."
    cat > "$ROOT_DIR/scripts/metrics.sh" << 'EOF'
#!/bin/bash

# Nightly Docker DevBox - Metrics Script
# View health metrics

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

show_usage() {
    echo "Usage: $0 [container_name]"
    echo ""
    echo "View health metrics for a Nightly DevBox container."
    echo ""
    echo "If no container name is specified, the script will find the first"
    echo "running Nightly DevBox container."
}

find_container() {
    local container_name=$1
    
    if [[ -n "$container_name" ]]; then
        # Check if specific container exists and is running
        if docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
            echo "$container_name"
            return 0
        else
            log_error "Container not found or not running: $container_name"
            return 1
        fi
    else
        # Find any running Nightly DevBox container
        local containers
        containers=$(docker ps --format "{{.Names}}" | grep "nightly-devbox" | head -1)
        
        if [[ -n "$containers" ]]; then
            echo "$containers"
            return 0
        else
            log_error "No running Nightly DevBox containers found"
            return 1
        fi
    fi
}

show_container_info() {
    local container_name=$1
    
    log_info "Container Information:"
    echo ""
    
    # Basic info
    echo "  Name: $container_name"
    echo "  Status: $(docker inspect --format='{{.State.Status}}' $container_name)"
    echo "  Health: $(docker inspect --format='{{.State.Health.Status}}' $container_name)"
    echo "  Image: $(docker inspect --format='{{.Config.Image}}' $container_name)"
    echo ""
    
    # Resource usage
    log_info "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}" $container_name
    echo ""
    
    # Port mappings
    log_info "Port Mappings:"
    docker port $container_name || echo "  No port mappings"
    echo ""
    
    # Volumes
    log_info "Volume Mappings:"
    docker inspect --format='{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' $container_name || echo "  No volume mappings"
    echo ""
    
    # Recent logs
    log_info "Recent Logs:"
    docker logs --tail 20 $container_name || echo "  No logs available"
}

main() {
    local container_name=${1:-""}
    
    if [[ "$container_name" == "-h" || "$container_name" == "--help" ]]; then
        show_usage
        exit 0
    fi
    
    log_info "Finding container..."
    container_name=$(find_container "$container_name") || exit 1
    
    show_container_info "$container_name"
}

main "$@"
EOF
    chmod +x "$ROOT_DIR/scripts/metrics.sh"
    log_success "Metrics script created"
}

create_cleanup_script() {
    log_info "Creating cleanup script..."
    cat > "$ROOT_DIR/scripts/cleanup.sh" << 'EOF'
#!/bin/bash

# Nightly Docker DevBox - Cleanup Script
# Clean up containers and images

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

show_usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Clean up Nightly DevBox containers and images."
    echo ""
    echo "Options:"
    echo "  -c, --containers    - Remove all Nightly DevBox containers"
    echo "  -i, --images        - Remove all Nightly DevBox images"
    echo "  -a, --all           - Remove containers and images"
    echo "  -h, --help          - Show this help"
}

cleanup_containers() {
    log_info "Finding Nightly DevBox containers..."
    local containers
    containers=$(docker ps -a --format "{{.Names}}" | grep "nightly-devbox")
    
    if [[ -z "$containers" ]]; then
        log_info "No Nightly DevBox containers found"
        return 0
    fi
    
    log_info "Stopping and removing containers..."
    echo "$containers" | while read container; do
        if [[ -n "$container" ]]; then
            log_info "Removing container: $container"
            docker rm -f "$container" 2>/dev/null || true
        fi
    done
    
    log_success "Containers cleaned up"
}

cleanup_images() {
    log_info "Finding Nightly DevBox images..."
    local images
    images=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep "nightly-devbox")
    
    if [[ -z "$images" ]]; then
        log_info "No Nightly DevBox images found"
        return 0
    fi
    
    log_info "Removing images..."
    echo "$images" | while read image; do
        if [[ -n "$image" ]]; then
            log_info "Removing image: $image"
            docker rmi -f "$image" 2>/dev/null || true
        fi
    done
    
    log_success "Images cleaned up"
}

main() {
    local cleanup_containers=false
    local cleanup_images=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -c|--containers)
                cleanup_containers=true
                shift
                ;;
            -i|--images)
                cleanup_images=true
                shift
                ;;
            -a|--all)
                cleanup_containers=true
                cleanup_images=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Default to cleaning both if no options specified
    if [[ "$cleanup_containers" == "false" && "$cleanup_images" == "false" ]]; then
        cleanup_containers=true
        cleanup_images=true
    fi
    
    if [[ "$cleanup_containers" == "true" ]]; then
        cleanup_containers
    fi
    
    if [[ "$cleanup_images" == "true" ]]; then
        cleanup_images
    fi
    
    log_success "Cleanup completed"
}

main "$@"
EOF
    chmod +x "$ROOT_DIR/scripts/cleanup.sh"
    log_success "Cleanup script created"
}

create_test_script() {
    log_info "Creating test script..."
    cat > "$ROOT_DIR/scripts/test.sh" << 'EOF'
#!/bin/bash

# Nightly Docker DevBox - Test Script
# Run tests for the development environment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

show_usage() {
    echo "Usage: $0 [test_type]"
    echo ""
    echo "Run tests for Nightly DevBox."
    echo ""
    echo "Test types:"
    echo "  unit        - Unit tests for scripts (default)"
    echo "  integration - Integration tests with Docker"
    echo "  all         - Run all tests"
    echo "  help        - Show this help"
}

test_unit() {
    log_info "Running unit tests..."
    
    # Test that all scripts are executable
    local scripts=(
        "$ROOT_DIR/scripts/build.sh"
        "$ROOT_DIR/scripts/run.sh"
        "$ROOT_DIR/scripts/console.sh"
        "$ROOT_DIR/scripts/metrics.sh"
        "$ROOT_DIR/scripts/cleanup.sh"
    )
    
    for script in "${scripts[@]}"; do
        if [[ -x "$script" ]]; then
            log_success "Script is executable: $(basename $script)"
        else
            log_error "Script is not executable: $(basename $script)"
            return 1
        fi
    done
    
    # Test that Dockerfiles exist
    local dockerfiles=(
        "$ROOT_DIR/dockerfiles/Dockerfile.python"
        "$ROOT_DIR/dockerfiles/Dockerfile.node"
        "$ROOT_DIR/dockerfiles/Dockerfile.rust"
        "$ROOT_DIR/dockerfiles/Dockerfile.go"
    )
    
    for dockerfile in "${dockerfiles[@]}"; do
        if [[ -f "$dockerfile" ]]; then
            log_success "Dockerfile exists: $(basename $dockerfile)"
        else
            log_error "Dockerfile missing: $(basename $dockerfile)"
            return 1
        fi
    done
    
    # Test that welcome art exists
    if [[ -f "$ROOT_DIR/assets/welcome.txt" ]]; then
        log_success "Welcome art exists"
    else
        log_error "Welcome art missing"
        return 1
    fi
    
    log_success "Unit tests passed"
}

test_integration() {
    log_info "Running integration tests..."
    
    # Check if Docker is available
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        return 1
    fi
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        return 1
    fi
    
    # Test building Python image
    log_info "Testing Python image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.python" -t "test-nightly-devbox-python" "$ROOT_DIR" 2>/dev/null; then
        log_success "Python image built successfully"
        docker rmi "test-nightly-devbox-python" 2>/dev/null || true
    else
        log_error "Python image build failed"
        return 1
    fi
    
    # Test building Node.js image
    log_info "Testing Node.js image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.node" -t "test-nightly-devbox-node" "$ROOT_DIR" 2>/dev/null; then
        log_success "Node.js image built successfully"
        docker rmi "test-nightly-devbox-node" 2>/dev/null || true
    else
        log_error "Node.js image build failed"
        return 1
    fi
    
    # Test building Rust image
    log_info "Testing Rust image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.rust" -t "test-nightly-devbox-rust" "$ROOT_DIR" 2>/dev/null; then
        log_success "Rust image built successfully"
        docker rmi "test-nightly-devbox-rust" 2>/dev/null || true
    else
        log_error "Rust image build failed"
        return 1
    fi
    
    # Test building Go image
    log_info "Testing Go image build..."
    if docker build -f "$ROOT_DIR/dockerfiles/Dockerfile.go" -t "test-nightly-devbox-go" "$ROOT_DIR" 2>/dev/null; then
        log_success "Go image built successfully"
        docker rmi "test-nightly-devbox-go" 2>/dev/null || true
    else
        log_error "Go image build failed"
        return 1
    fi
    
    log_success "Integration tests passed"
}

main() {
    local test_type=${1:-"unit"}
    
    case $test_type in
        unit)
            test_unit
            ;;
        integration)
            test_integration
            ;;
        all)
            test_unit
            test_integration
            ;;
        help)
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown test type: $test_type"
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
EOF
    chmod +x "$ROOT_DIR/scripts/test.sh"
    log_success "Test script created"
}

main() {
    log_info "Building Nightly Docker DevBox..."
    
    check_docker
    create_directories
    create_welcome_art
    create_dockerfile_python
    create_dockerfile_node
    create_dockerfile_rust
    create_dockerfile_go
    create_run_script
    create_console_script
    create_metrics_script
    create_cleanup_script
    create_test_script
    
    log_success "Nightly Docker DevBox built successfully!"
    log_info "Run './scripts/run.sh python' to start your development environment"
}

main "$@"
