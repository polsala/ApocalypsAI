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
