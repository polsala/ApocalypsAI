#!/bin/bash

# Whimsical messages
MSG_WELCOME="Welcome to the Nightly Container Critter Catcher!"
MSG_SCANNING="Scanning for digital critters..."
MSG_NO_CRITTERS="No critters found! Your Docker environment is sparkling clean."
MSG_PROMPT_CLEANUP="Would you like to rehome these critters? (y/N): "
MSG_REHOMING_CONTAINER="Rehoming Sleepy Critter %s (%s)..."
MSG_REHOMING_IMAGE="Rehoming Lost Pup %s..."
MSG_REHOMING_VOLUME="Rehoming Forgotten Nest %s..."
MSG_DONE="Done!"
MSG_SKIPPING="Skipping cleanup. Critters get to stay for now!"
MSG_ALL_REHOMED="All identified critters have been rehomed. Your Docker environment is now a bit tidier!"
MSG_INVALID_COMMAND="Invalid command. Usage: critter_catcher.sh [scan|cleanup]"

# Function to find stopped containers (Sleepy Critters)
find_stopped_containers() {
    docker ps -aq -f status=exited
}

# Function to find dangling images (Lost Pups)
find_dangling_images() {
    docker images -f "dangling=true" -q
}

# Function to find unused volumes (Forgotten Nests)
find_unused_volumes() {
    # Docker volumes ls -qf "dangling=true" only shows volumes not used by any container
    # This is equivalent to `docker volume prune` target
    docker volume ls -qf "dangling=true"
}

# Function to get container name/image for display
get_container_info() {
    local container_id="$1"
    docker inspect --format '{{.Name}} ({{.Config.Image}})' "$container_id" 2>/dev/null | sed 's/^\///'
}

# Function to get image tag/ID for display
get_image_info() {
    local image_id="$1"
    docker images --format '{{.Repository}}:{{.Tag}} (Image ID: {{.ID}})' -f "id=$image_id" 2>/dev/null | head -n 1
}

# Main logic
main() {
    echo "$MSG_WELCOME"
    echo "$MSG_SCANNING"
    echo

    local stopped_containers=$(find_stopped_containers)
    local dangling_images=$(find_dangling_images)
    local unused_volumes=$(find_unused_volumes)

    local total_critters=0

    if [ -n "$stopped_containers" ]; then
        echo "Found $(echo "$stopped_containers" | wc -l) Sleepy Critters (stopped containers):"
        for id in $stopped_containers; do
            info=$(get_container_info "$id")
            printf "  - %s (%s)\n" "$id" "$info"
        done
        total_critters=$((total_critters + $(echo "$stopped_containers" | wc -l)))
        echo
    else
        echo "Found 0 Sleepy Critters (stopped containers)."
        echo
    fi

    if [ -n "$dangling_images" ]; then
        echo "Found $(echo "$dangling_images" | wc -l) Lost Pups (dangling images):"
        for id in $dangling_images; do
            info=$(get_image_info "$id")
            printf "  - %s\n" "$info"
        done
        total_critters=$((total_critters + $(echo "$dangling_images" | wc -l)))
        echo
    else
        echo "Found 0 Lost Pups (dangling images)."
        echo
    fi

    if [ -n "$unused_volumes" ]; then
        echo "Found $(echo "$unused_volumes" | wc -l) Forgotten Nests (unused volumes):"
        for id in $unused_volumes; do
            printf "  - %s\n" "$id"
        done
        total_critters=$((total_critters + $(echo "$unused_volumes" | wc -l)))
        echo
    else
        echo "Found 0 Forgotten Nests (unused volumes)."
        echo
    fi

    if [ "$total_critters" -eq 0 ]; then
        echo "$MSG_NO_CRITTERS"
        return 0
    fi

    # If command is 'scan', just report and exit
    if [ "$1" == "scan" ]; then
        return 0
    fi

    # If command is 'cleanup' (or default), prompt for action
    read -p "$MSG_PROMPT_CLEANUP" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo

        # Rehome stopped containers
        if [ -n "$stopped_containers" ]; then
            for id in $stopped_containers; do
                info=$(get_container_info "$id")
                printf "$MSG_REHOMING_CONTAINER\n" "$id" "$info"
                docker rm "$id" >/dev/null 2>&1
            done
        fi

        # Rehome dangling images
        if [ -n "$dangling_images" ]; then
            for id in $dangling_images; do
                info=$(get_image_info "$id")
                printf "$MSG_REHOMING_IMAGE\n" "$info"
                docker rmi "$id" >/dev/null 2>&1
            done
        fi

        # Rehome unused volumes
        if [ -n "$unused_volumes" ]; then
            for id in $unused_volumes; do
                printf "$MSG_REHOMING_VOLUME\n" "$id"
                docker volume rm "$id" >/dev/null 2>&1
            done
        fi

        echo
        echo "$MSG_ALL_REHOMED"
    else
        echo "$MSG_SKIPPING"
    fi
}

# Handle arguments
case "$1" in
    scan)
        main "scan"
        ;;
    cleanup)
        main "cleanup"
        ;;
    "") # Default to cleanup if no argument provided
        main "cleanup"
        ;;
    *)
        echo "$MSG_INVALID_COMMAND"
        exit 1
        ;;
esac
