#!/bin/bash

IMAGE_NAME="focus-bubble-pod"
CONTAINER_NAME="focus-bubble-instance"
DATA_DIR="focus_data"

# Function to build the Docker image
function build_image() {
    echo "Building the Focus Bubble Pod image..."
    docker build -t "$IMAGE_NAME" src/
    if [ $? -eq 0 ]; then
        echo "Focus Bubble Pod image built successfully!"
    else
        echo "Failed to build Focus Bubble Pod image."
        exit 1
    fi
}

# Function to start a new focus bubble container
function start_bubble() {
    # Check if image exists, build if not
    if ! docker images -q "$IMAGE_NAME" > /dev/null; then
        echo "Image '$IMAGE_NAME' not found. Building it first..."
        build_image
        if [ $? -ne 0 ]; then
            echo "Failed to build image, cannot start bubble."
            exit 1
        fi
    fi

    # Check if container is already running or stopped
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "Focus Bubble Pod is already running or stopped. Please stop/remove it first."
        exit 1
    fi

    # Create data directory if it doesn't exist
    mkdir -p "$DATA_DIR"

    echo "Starting your ephemeral Focus Bubble Pod. Your work in '$DATA_DIR' will persist."
    echo "Type 'exit' to leave the bubble. The container will be removed automatically."
    docker run -it --rm -v "$(pwd)/$DATA_DIR:/app/data" --name "$CONTAINER_NAME" "$IMAGE_NAME" bash -c "cowsay 'Welcome to your Focus Bubble! Your thoughts are safe here. Your data is in /app/data.'; bash"
    echo "Focus Bubble Pod session ended."
}

# Function to stop a running focus bubble container
function stop_bubble() {
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "Stopping the Focus Bubble Pod..."
        docker stop "$CONTAINER_NAME"
        echo "Focus Bubble Pod stopped."
    else
        echo "Focus Bubble Pod is not running."
    fi
}

# Function to clean up the image and any stopped containers
function clean_all() {
    echo "Cleaning up Focus Bubble Pod container and image..."
    # Remove any stopped container first
    if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        docker rm -f "$CONTAINER_NAME" > /dev/null 2>&1
        echo "Removed stopped container '$CONTAINER_NAME'."
    fi
    
    # Remove the image
    if docker images -q "$IMAGE_NAME" > /dev/null; then
        docker rmi "$IMAGE_NAME"
        echo "Focus Bubble Pod image removed."
    else
        echo "Focus Bubble Pod image not found."
    fi
    
    if [ -d "$DATA_DIR" ]; then
        echo "Keeping your '$DATA_DIR' for future bubbles. Remove it manually if not needed."
    fi
    echo "Cleanup complete."
}

# Main script logic based on arguments
case "$1" in
    build)
        build_image
        ;;
    start)
        start_bubble
        ;;
    stop)
        stop_bubble
        ;;
    clean)
        clean_all
        ;;
    *)
        echo "Usage: $0 {build|start|stop|clean}"
        exit 1
        ;;
esac
