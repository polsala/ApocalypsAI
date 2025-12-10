#!/bin/bash

# Default to bash if no argument is provided
LANGUAGE=${1:-bash}

case "$LANGUAGE" in
    python)
        echo "Starting Python 3.11 environment..."
        exec python3 "$@"
        ;;
    node)
        echo "Starting Node.js 20 environment..."
        exec node "$@"
        ;;
    rust)
        echo "Starting Rust 1.70 environment..."
        exec cargo "$@"
        ;;
    go)
        echo "Starting Go 1.21 environment..."
        exec go "$@"
        ;;
    bash)
        echo "Starting a generic bash shell..."
        exec bash "$@"
        ;;
    *)
        echo "Unsupported language: $LANGUAGE. Available: python, node, rust, go, bash."
        exit 1
        ;;
esac
