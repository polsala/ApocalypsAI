#!/bin/bash

# ApocalypsAI Docker Environment Manager Entrypoint

# Function to display available environments
list_environments() {
    echo "Available environments:"
    echo "  python-env"
    echo "  node-env"
    echo "  go-env"
}

# Main logic
case "$1" in
    python-env)
        echo "Starting Python development environment..."
        exec /bin/bash
        ;;
    node-env)
        echo "Starting Node.js development environment..."
        exec /bin/bash
        ;;
    go-env)
        echo "Starting Go development environment..."
        exec /bin/bash
        ;;
    list-envs)
        list_environments
        ;;
    *)
        echo "Error: Unknown command '$1'"
        list_environments
        exit 1
        ;;
esac
