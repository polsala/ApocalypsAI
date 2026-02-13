#!/bin/bash

set -euo pipefail

# Helper function to display usage
usage() {
    echo "Usage: garden <command> [options]"
    echo ""
    echo "Commands:"
    echo "  grow    [compose_file]  Start the container garden defined by compose_file (default: docker-compose.yml)"
    echo "  harvest [compose_file]  Stop and remove the container garden defined by compose_file (default: docker-compose.yml)"
    echo "  weed                    Prune all unused Docker system resources (images, containers, volumes, networks)"
    echo "  status  [compose_file]  Show the status of containers in the garden defined by compose_file (default: docker-compose.yml)"
    echo "  --help                  Display this help message"
    echo ""
    echo "Options for grow/harvest/status:"
    echo "  -f, --file <path>       Specify an alternate compose file (default: docker-compose.yml)"
    echo ""
    echo "Examples:"
    echo "  garden grow -f my-dev-stack.yml"
    echo "  garden status"
    echo "  garden weed"
}

# Parse options for commands that accept -f/--file
parse_compose_options() {
    local default_file="docker-compose.yml"
    local compose_file="$default_file"
    local args=()
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -f|--file)
                if [[ -n "$2" && ! "$2" =~ ^- ]]; then
                    compose_file="$2"
                    shift
                else
                    echo "Error: Argument for $1 is missing." >&2
                    exit 1
                fi
                ;;
            *)
                args+=("$1") # Collect other arguments
                ;;
        esac
        shift
    done
    echo "$compose_file" "${args[@]}"
}

# Function to get project name from compose file path
get_project_name() {
    local compose_file="$1"
    local project_dir
    project_dir=$(dirname "$compose_file")
    if [[ "$project_dir" == "." ]]; then
        project_dir=$(pwd)
    fi
    # Sanitize project name: lowercase, alphanumeric and hyphens only
    basename "$project_dir" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]-' | sed 's/^-*//;s/-*$//'
}


# Main logic
if [[ $# -eq 0 ]]; then
    usage
    exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
    grow|harvest|status)
        # Parse options for these commands
        read -r COMPOSE_FILE REST_ARGS <<< "$(parse_compose_options "$@")"
        set -- "$REST_ARGS" # Reset positional parameters for potential future use, though not strictly needed here

        if [[ ! -f "$COMPOSE_FILE" ]]; then
            echo "Error: Compose file '$COMPOSE_FILE' not found." >&2
            exit 1
        fi
        PROJECT_NAME=$(get_project_name "$COMPOSE_FILE")

        case "$COMMAND" in
            grow)
                echo "Cultivating garden '$PROJECT_NAME' from '$COMPOSE_FILE'..."
                docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" up -d --build
                echo "Garden '$PROJECT_NAME' is growing!"
                ;;
            harvest)
                echo "Harvesting garden '$PROJECT_NAME' from '$COMPOSE_FILE'..."
                docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" down --volumes --remove-orphans
                echo "Garden '$PROJECT_NAME' harvested."
                ;;
            status)
                echo "Inspecting garden '$PROJECT_NAME' from '$COMPOSE_FILE'..."
                docker compose -f "$COMPOSE_FILE" -p "$PROJECT_NAME" ps
                ;;
        esac
        ;;
    weed)
        if [[ $# -gt 0 ]]; then
            echo "Error: 'weed' command does not accept arguments." >&2
            usage
            exit 1
        fi
        echo "Weeding all unused Docker system resources (images, containers, volumes, networks)..."
        docker system prune -f --volumes
        echo "Global weeding complete!"
        ;;
    --help|-h)
        usage
        exit 0
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'" >&2
        usage
        exit 1
        ;;
esac
