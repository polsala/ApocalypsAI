#!/bin/bash

IMAGE_NAME="chrono-vault-cli"
CONTAINER_NAME="chrono-vault-instance"

function build_image() {
    echo "Building Docker image: $IMAGE_NAME..."
    docker build -t "$IMAGE_NAME" .
    if [ $? -eq 0 ]; then
        echo "Image '$IMAGE_NAME' built successfully."
    else
        echo "Failed to build image '$IMAGE_NAME'."
        exit 1
    fi
}

function run_interactive() {
    echo "Running interactive shell in container: $IMAGE_NAME..."
    docker run -it --rm --name "$CONTAINER_NAME" "$IMAGE_NAME" bash
}

function execute_command() {
    if [ -z "$1" ]; then
        echo "Error: No command provided for 'exec'."
        echo "Usage: $0 exec \"<command>\""
        exit 1
    fi
    echo "Executing command in container: $IMAGE_NAME..."
    docker run --rm "$IMAGE_NAME" bash -c "$1"
}

case "$1" in
    build)
        build_image
        ;;
    run)
        run_interactive
        ;;
    exec)
        shift # Remove 'exec' from arguments
        execute_command "$@"
        ;;
    *)
        echo "Usage: $0 {build|run|exec \"<command>\"}"
        exit 1
        ;;
esac
