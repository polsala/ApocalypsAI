#!/bin/bash

# Nightly Docker DevBox
# A whimsical-yet-useful containerized development environment generator

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/templates"
WORKSPACES_DIR="$HOME/.devbox/workspaces"
LOG_FILE="$HOME/.devbox/devbox.log"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    log "ERROR: $1"
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
    log "SUCCESS: $1"
}

# Warning message
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
    log "WARNING: $1"
}

# Info message
info() {
    echo -e "${BLUE}ℹ $1${NC}"
    log "INFO: $1"
}

# Check dependencies
check_dependencies() {
    local missing=()
    
    command -v docker >/dev/null 2>&1 || missing+=("docker")
    command -v docker-compose >/dev/null 2>&1 || missing+=("docker-compose")
    command -v jq >/dev/null 2>&1 || missing+=("jq")
    
    if [ ${#missing[@]} -ne 0 ]; then
        error_exit "Missing required dependencies: ${missing[*]}. Please install them and try again."
    fi
    
    # Check Docker daemon
    if ! docker info >/dev/null 2>&1; then
        error_exit "Docker daemon is not running. Please start Docker and try again."
    fi
}

# Initialize directories
init_directories() {
    mkdir -p "$WORKSPACES_DIR"
    mkdir -p "$LOG_FILE"
}

# Show help
show_help() {
    cat << EOF
${CYAN}Nightly Docker DevBox${NC}
A whimsical-yet-useful containerized development environment generator

${PURPLE}USAGE:${NC}
    $0 [OPTIONS]

${PURPLE}OPTIONS:${NC}
    -t, --template <name>     Template name (python, nodejs, rust, go, etc.)
    -n, --name <name>         Project name
    -l, --list-templates      List available templates
    -s, --start               Start existing environment
    -p, --stop                Stop running environment
    -r, --remove              Remove environment
    -e, --exec                Execute command in running container
    -c, --command <cmd>       Command to execute (used with --exec)
    -i, --interactive         Force interactive mode
    -h, --help                Show this help message

${PURPLE}EXAMPLES:${NC}
    $0 --template python --name my-python-app
    $0 --start --name my-python-app
    $0 --exec --name my-python-app --command "python app.py"
    $0 --list-templates
    $0                              # Interactive mode

${PURPLE}TEMPLATES:${NC}
    Use --list-templates to see all available development environments.

EOF
}

# List available templates
list_templates() {
    info "Available development environment templates:"
    echo
    
    if [ ! -d "$TEMPLATES_DIR" ]; then
        error_exit "Templates directory not found: $TEMPLATES_DIR"
    fi
    
    for template_file in "$TEMPLATES_DIR"/*.json; do
        if [ -f "$template_file" ]; then
            local name=$(basename "$template_file" .json)
            local description=$(jq -r '.description // "No description available"' "$template_file")
            echo -e "  ${GREEN}$name${NC}: $description"
        fi
    done
    echo
}

# Validate template
validate_template() {
    local template_file="$1"
    
    if [ ! -f "$template_file" ]; then
        error_exit "Template file not found: $template_file"
    fi
    
    # Basic JSON validation
    if ! jq empty "$template_file" 2>/dev/null; then
        error_exit "Invalid JSON in template: $template_file"
    fi
    
    # Check required fields
    local required_fields=("name" "description" "dockerfile")
    for field in "${required_fields[@]}"; do
        if ! jq -e ".${field}" "$template_file" >/dev/null 2>&1; then
            error_exit "Missing required field '$field' in template: $template_file"
        fi
    done
}

# Get template information
get_template_info() {
    local template_name="$1"
    local template_file="$TEMPLATES_DIR/${template_name}.json"
    
    validate_template "$template_file"
    
    echo "$template_file"
}

# Generate Docker Compose configuration
generate_compose_config() {
    local template_file="$1"
    local project_name="$2"
    local workspace_dir="$3"
    
    local service_name="devbox-${project_name}"
    local image_name="devbox-${template_name}:latest"
    
    # Read template configuration
    local dockerfile=$(jq -r '.dockerfile' "$template_file")
    local ports=$(jq -r '.ports // [] | join(",")' "$template_file")
    local environment=$(jq -r '.environment // {}' "$template_file")
    local startup_command=$(jq -r '.startup_command // ""' "$template_file")
    
    # Generate docker-compose.yml
    cat > "$workspace_dir/docker-compose.yml" << EOF
version: '3.8'

services:
  $service_name:
    build:
      context: .
      dockerfile: $dockerfile
    container_name: $service_name
    restart: unless-stopped
    volumes:
      - ./src:/app/src:cached
      - ./data:/app/data:cached
    working_dir: /app
    environment:
$(echo "$environment" | jq -r 'to_entries[] | "      " + .key + ": \"" + .value + "\"")
$(if [ -n "$ports" ]; then
        echo "    ports:"
        IFS=',' read -ra PORTS <<< "$ports"
        for port in "${PORTS[@]}"; do
            echo "      - \"$port:$port\""
        done
    fi)
$(if [ -n "$startup_command" ]; then
        echo "    command: $startup_command"
    fi)
    stdin_open: true
    tty: true
EOF
}

# Generate Dockerfile
generate_dockerfile() {
    local template_file="$1"
    local workspace_dir="$2"
    
    local dockerfile_name=$(jq -r '.dockerfile' "$template_file")
    local base_image=$(jq -r '.base_image // "ubuntu:22.04"' "$template_file")
    local packages=$(jq -r '.packages // [] | join(" ")' "$template_file")
    local startup_command=$(jq -r '.startup_command // ""' "$template_file")
    
    # If template provides a custom Dockerfile, copy it
    if [ -f "$TEMPLATES_DIR/$dockerfile_name" ]; then
        cp "$TEMPLATES_DIR/$dockerfile_name" "$workspace_dir/Dockerfile"
        return 0
    fi
    
    # Generate a basic Dockerfile
    cat > "$workspace_dir/Dockerfile" << EOF
# Generated Dockerfile for $template_name development environment
FROM $base_image

# Set working directory
WORKDIR /app

# Install packages if specified
$(if [ -n "$packages" ]; then
    echo "RUN apt-get update && apt-get install -y \
    $packages \
    && rm -rf /var/lib/apt/lists/*"
fi)

# Create source directory
RUN mkdir -p /app/src /app/data

# Set permissions
RUN useradd -m -s /bin/bash devuser && chown -R devuser:devuser /app
USER devuser

# Default command
$(if [ -n "$startup_command" ]; then
    echo "CMD [\"$startup_command\"]"
else
    echo "CMD [\"/bin/bash\"]"
fi)
EOF
}

# Create workspace directory
create_workspace() {
    local project_name="$1"
    local workspace_dir="$WORKSPACES_DIR/$project_name"
    
    if [ -d "$workspace_dir" ]; then
        warning "Workspace already exists: $workspace_dir"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error_exit "Workspace creation cancelled"
        fi
        rm -rf "$workspace_dir"
    fi
    
    mkdir -p "$workspace_dir/src"
    mkdir -p "$workspace_dir/data"
    
    success "Created workspace: $workspace_dir"
    echo "$workspace_dir"
}

# Build and start environment
start_environment() {
    local workspace_dir="$1"
    
    info "Building and starting development environment..."
    
    cd "$workspace_dir"
    
    # Build the image
    if ! docker-compose build; then
        error_exit "Failed to build Docker image"
    fi
    
    # Start the container
    if ! docker-compose up -d; then
        error_exit "Failed to start container"
    fi
    
    success "Development environment started!"
    
    # Show connection info
    info "Container is running. Connect with:"
    echo "  docker exec -it devbox-${project_name} /bin/bash"
    echo "  Or use: $0 --exec --name $project_name --command \"your command\"
}

# Stop environment
stop_environment() {
    local project_name="$1"
    local workspace_dir="$WORKSPACES_DIR/$project_name"
    
    if [ ! -d "$workspace_dir" ]; then
        error_exit "Workspace not found: $workspace_dir"
    fi
    
    cd "$workspace_dir"
    
    if ! docker-compose down; then
        error_exit "Failed to stop container"
    fi
    
    success "Development environment stopped"
}

# Remove environment
remove_environment() {
    local project_name="$1"
    local workspace_dir="$WORKSPACES_DIR/$project_name"
    
    if [ ! -d "$workspace_dir" ]; then
        error_exit "Workspace not found: $workspace_dir"
    fi
    
    read -p "Are you sure you want to remove '$project_name'? This cannot be undone. (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "Removal cancelled"
        return 0
    fi
    
    cd "$workspace_dir"
    
    if ! docker-compose down -v; then
        error_exit "Failed to remove container and volumes"
    fi
    
    rm -rf "$workspace_dir"
    
    success "Development environment removed"
}

# Execute command in running container
execute_command() {
    local project_name="$1"
    local command="$2"
    local workspace_dir="$WORKSPACES_DIR/$project_name"
    
    if [ ! -d "$workspace_dir" ]; then
        error_exit "Workspace not found: $workspace_dir"
    fi
    
    cd "$workspace_dir"
    
    if ! docker-compose exec -T devbox-$project_name $command; then
        error_exit "Failed to execute command in container"
    fi
}

# Interactive mode
interactive_mode() {
    echo -e "${CYAN}Welcome to Nightly Docker DevBox!${NC}"
    echo -e "${PURPLE}Let's create your perfect development environment together.\n${NC}"
    
    # Show available templates
    list_templates
    
    # Get template choice
    echo -n "${BLUE}Enter template name: ${NC}"
    read -r template_name
    
    # Validate template
    template_file=$(get_template_info "$template_name") || exit 1
    
    # Get project name
    echo -n "${BLUE}Enter project name: ${NC}"
    read -r project_name
    
    if [ -z "$project_name" ]; then
        error_exit "Project name cannot be empty"
    fi
    
    # Confirm creation
    echo
    echo -e "${YELLOW}Summary:${NC}"
    echo "  Template: $template_name"
    echo "  Project:  $project_name"
    echo
    read -p "Create this development environment? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        info "Creation cancelled"
        return 0
    fi
    
    # Create and start environment
    workspace_dir=$(create_workspace "$project_name")
    generate_dockerfile "$template_file" "$workspace_dir"
    generate_compose_config "$template_file" "$project_name" "$workspace_dir"
    start_environment "$workspace_dir"
}

# Main function
main() {
    local template_name=""
    local project_name=""
    local action=""
    local command=""
    local interactive=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -t|--template)
                template_name="$2"
                shift 2
                ;;
            -n|--name)
                project_name="$2"
                shift 2
                ;;
            -l|--list-templates)
                list_templates
                exit 0
                ;;
            -s|--start)
                action="start"
                shift
                ;;
            -p|--stop)
                action="stop"
                shift
                ;;
            -r|--remove)
                action="remove"
                shift
                ;;
            -e|--exec)
                action="exec"
                shift
                ;;
            -c|--command)
                command="$2"
                shift 2
                ;;
            -i|--interactive)
                interactive=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                error_exit "Unknown option: $1"
                ;;
        esac
    done
    
    # Initialize
    check_dependencies
    init_directories
    
    # Determine action
    if [ "$interactive" = true ] || { [ -z "$template_name" ] && [ -z "$action" ]; }; then
        interactive_mode
        exit 0
    fi
    
    # Validate required parameters
    if [ -z "$project_name" ]; then
        error_exit "Project name is required. Use --name or --help for usage."
    fi
    
    # Execute action
    case "$action" in
        start)
            start_environment "$WORKSPACES_DIR/$project_name"
            ;;
        stop)
            stop_environment "$project_name"
            ;;
        remove)
            remove_environment "$project_name"
            ;;
        exec)
            if [ -z "$command" ]; then
                error_exit "Command is required for exec action. Use --command."
            fi
            execute_command "$project_name" "$command"
            ;;
        "")
            # Create new environment
            if [ -z "$template_name" ]; then
                error_exit "Template name is required. Use --template or --help for usage."
            fi
            
            template_file=$(get_template_info "$template_name") || exit 1
            workspace_dir=$(create_workspace "$project_name")
            generate_dockerfile "$template_file" "$workspace_dir"
            generate_compose_config "$template_file" "$project_name" "$workspace_dir"
            start_environment "$workspace_dir"
            ;;
        *)
            error_exit "Unknown action: $action"
            ;;
    esac
}

# Run main function with all arguments
main "$@"
