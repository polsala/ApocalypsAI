#!/bin/bash

set -euo pipefail

CHAMBER_DIR="$HOME/.nightly-temporal-dev-chamber"
CHAMBER_CONFIG="$CHAMBER_DIR/chambers.conf"

mkdir -p "$CHAMBER_DIR"
touch "$CHAMBER_CONFIG"

log_error() {
    echo "Error: $1" >&2
    exit 1
}

log_info() {
    echo "Info: $1"
}

build_chamber() {
    local chamber_name="$1"
    local base_image="$2"
    local setup_commands="$3"

    if grep -q "^${chamber_name}:" "$CHAMBER_CONFIG"; then
        log_error "Chamber '$chamber_name' already exists. Use a different name or remove it first."
    fi

    log_info "Building temporal chamber '$chamber_name' with base image '$base_image'\n"

    local temp_dockerfile_dir
    temp_dockerfile_dir=$(mktemp -d)
    local dockerfile_path="$temp_dockerfile_dir/Dockerfile"

    cat > "$dockerfile_path" <<EOF
FROM ${base_image}
WORKDIR /app

# Install setup commands if provided
$(if [ -n "$setup_commands" ]; then echo "RUN ${setup_commands}"; fi)

CMD ["bash"]
EOF

    log_info "Generated Dockerfile at $dockerfile_path:\n$(cat "$dockerfile_path")\n"

    if ! docker build -t "nightly-temporal-dev-chamber-${chamber_name}" "$temp_dockerfile_dir"; then
        rm -rf "$temp_dockerfile_dir"
        log_error "Failed to build Docker image for chamber '$chamber_name'."
    fi

    echo "${chamber_name}:${base_image}:${setup_commands}" >> "$CHAMBER_CONFIG"
    log_info "Chamber '$chamber_name' built and configured successfully."
    rm -rf "$temp_dockerfile_dir"
}

run_chamber() {
    local chamber_name="$1"
    local command="${2:-bash}"

    if ! grep -q "^${chamber_name}:" "$CHAMBER_CONFIG"; then
        log_error "Chamber '$chamber_name' not found. Please build it first."
    fi

    log_info "Running temporal chamber '$chamber_name' with command: '$command'"
    docker run -it --rm -v "$(pwd):/app" -w /app "nightly-temporal-dev-chamber-${chamber_name}" "$command"
}

list_chambers() {
    log_info "Available Temporal Chambers:"
    if [ ! -s "$CHAMBER_CONFIG" ]; then
        echo "  No chambers configured yet."
        return 0
    fi

    while IFS=':' read -r name image setup;
    do
        echo "  - Name: $name"
        echo "    Base Image: $image"
        [ -n "$setup" ] && echo "    Setup Commands: $setup"
        echo ""
    done < "$CHAMBER_CONFIG"
}

case "$1" in
    build)
        if [ "$#" -lt 3 ]; then
            log_error "Usage: $0 build <chamber_name> <base_image> [setup_commands]"
        fi
        build_chamber "$2" "$3" "${4:-}"
        ;;
    run)
        if [ "$#" -lt 2 ]; then
            log_error "Usage: $0 run <chamber_name> [command]"
        fi
        run_chamber "$2" "${3:-}"
        ;;
    list)
        list_chambers
        ;;
    *)
        log_error "Unknown command: $1. Usage: $0 {build|run|list}"
        ;;
esac
