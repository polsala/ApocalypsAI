#!/bin/bash

set -euo pipefail

IMAGE_NAME="temporal-echo-chamber"

function build_chamber() {
    local era_tag="$1"
    local python_version="${2:-3.9}" # Default to 3.9 if not specified

    echo "Building Temporal Echo Chamber for era: ${era_tag} (Python ${python_version})..."
    docker build -t "${IMAGE_NAME}:${era_tag}" --build-arg PYTHON_VERSION="${python_version}" .
    echo "Build complete: ${IMAGE_NAME}:${era_tag}"
}

function run_chamber() {
    local era_tag="$1"
    shift
    local command="${@:-bash}" # Default to bash if no command provided

    echo "Entering Temporal Echo Chamber for era: ${era_tag} with command: '${command}'"
    docker run --rm -it "${IMAGE_NAME}:${era_tag}" "${command}"
}

function cleanup_chamber() {
    local era_tag="$1"
    echo "Cleaning up Temporal Echo Chamber image: ${IMAGE_NAME}:${era_tag}"
    docker rmi "${IMAGE_NAME}:${era_tag}" || true # Ignore error if image doesn't exist
}

case "$1" in
    build)
        if [ -z "$2" ]; then
            echo "Usage: $0 build <era_tag> [python_version]"
            exit 1
        fi
        build_chamber "$2" "$3"
        ;;
    run)
        if [ -z "$2" ]; then
            echo "Usage: $0 run <era_tag> [command...]"
            exit 1
        fi
        run_chamber "$2" "${@:3}"
        ;;
    cleanup)
        if [ -z "$2" ]; then
            echo "Usage: $0 cleanup <era_tag>"
            exit 1
        fi
        cleanup_chamber "$2"
        ;;
    *)
        echo "Usage: $0 {build|run|cleanup} ..."
        exit 1
        ;;
esac
