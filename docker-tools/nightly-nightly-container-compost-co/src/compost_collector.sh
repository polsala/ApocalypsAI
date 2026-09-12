#!/bin/bash

set -euo pipefail

DRY_RUN=true

# Function to print whimsical messages
print_whimsical() {
    echo -e "$1"
}

# Parse arguments
for arg in "$@"; do
    case $arg in
        --force)
            DRY_RUN=false
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            print_whimsical "Unknown argument: $arg. Defaulting to dry run."
            shift
            ;;
    esac
done

print_whimsical "🌿 Nightly Container Compost Collector Initiated 🌿\n"
print_whimsical "Scanning for digital detritus...\n"

# Find exited containers
EXPIRED_CONTAINERS=$(docker ps -a --filter "status=exited" --format "{{.ID}}\t{{.Status}}\t{{.Names}}" || true)
NUM_EXPIRED_CONTAINERS=$(echo "$EXPIRED_CONTAINERS" | grep -c . || true)

# Find dangling images
DANGLING_IMAGES=$(docker images --filter "dangling=true" --format "{{.ID}}\t{{.Repository}}\t{{.Tag}}" || true)
NUM_DANGLING_IMAGES=$(echo "$DANGLING_IMAGES" | grep -c . || true)

# Find dangling volumes
DANGLING_VOLUMES=$(docker volume ls --filter "dangling=true" --format "{{.Name}}" || true)
NUM_DANGLING_VOLUMES=$(echo "$DANGLING_VOLUMES" | grep -c . || true)

TOTAL_COMPOSTABLES=$((NUM_EXPIRED_CONTAINERS + NUM_DANGLING_IMAGES + NUM_DANGLING_VOLUMES))

if [ "$NUM_EXPIRED_CONTAINERS" -gt 0 ]; then
    print_whimsical "Found $NUM_EXPIRED_CONTAINERS exited container(s) ready for composting:"
    echo "$EXPIRED_CONTAINERS" | while IFS=$'\t' read -r ID STATUS NAME; do
        print_whimsical "  - Container ID: ${ID:0:12}, Name: $NAME"
    done
else
    print_whimsical "No exited containers found. All active or recently stopped!"
fi

if [ "$NUM_DANGLING_IMAGES" -gt 0 ]; then
    print_whimsical "\nFound $NUM_DANGLING_IMAGES dangling image(s) for decomposition:"
    echo "$DANGLING_IMAGES" | while IFS=$'\t' read -r ID REPO TAG; do
        print_whimsical "  - Image ID: ${ID:0:12}, Repository: $REPO, Tag: $TAG"
    done
else
    print_whimsical "\nNo dangling images found. Your image registry is pristine!"
fi

if [ "$NUM_DANGLING_VOLUMES" -gt 0 ]; then
    print_whimsical "\nFound $NUM_DANGLING_VOLUMES unused volume(s) to return to the earth:"
    echo "$DANGLING_VOLUMES" | while IFS=$'\t' read -r NAME; do
        print_whimsical "  - Volume Name: $NAME"
    done
else
    print_whimsical "\nNo unused volumes found. Your storage is efficiently utilized!"
fi

print_whimsical "\n"

if [ "$DRY_RUN" = true ]; then
    if [ "$TOTAL_COMPOSTABLES" -gt 0 ]; then
        print_whimsical "This was a dry run. No resources were composted. To proceed, run with '--force'."
    else
        print_whimsical "No digital detritus found. Your garden is already sparkling clean!"
    fi
    print_whimsical "🌱 Your digital garden awaits its refresh! 🌱"
else
    if [ "$TOTAL_COMPOSTABLES" -gt 0 ]; then
        print_whimsical "Initiating digital decomposition...\n"
        # Perform the actual pruning
        docker system prune --all --force --volumes
        print_whimsical "\nComposting complete! Your digital garden is refreshed."
        print_whimsical "✨ Enjoy the clean, fertile ground for new growth! ✨"
    else
        print_whimsical "No digital detritus found. Nothing to compost!"
        print_whimsical "✨ Your digital garden is already perfectly clean! ✨"
    fi
fi
