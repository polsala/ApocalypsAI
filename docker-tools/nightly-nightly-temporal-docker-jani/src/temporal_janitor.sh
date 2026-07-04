#!/bin/bash
set -euo pipefail

# Default values
DAYS_OLD=7
DRY_RUN=false
FORCE_REMOVE=false

# Whimsical messages for the temporal janitor
MESSAGES=(
    "The temporal janitor is sweeping through forgotten timelines..."
    "Dusting off the cobwebs of past computations..."
    "Reclaiming disk space from the echoes of yesterday..."
    "Ensuring the multiverse of containers remains spick and span..."
    "A whisper from the void: 'Time to declutter!'"
    "Erasing temporal paradoxes from your storage drives..."
    "Cleaning up the chronological residue of Docker's past..."
)

# Function to display a random whimsical message
display_whimsical_message() {
    local index=$(( RANDOM % ${#MESSAGES[@]} ))
    echo "🌌 ${MESSAGES[$index]}"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --days-old)
            DAYS_OLD="$2"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            ;;
        --force)
            FORCE_REMOVE=true
            ;;
        -h|--help)
            echo "Usage: $(basename "$0") [--days-old N] [--dry-run] [--force]"
            echo "  --days-old N: Remove exited containers older than N days (default: 7)."
            echo "  --dry-run: Simulate cleanup without making actual changes."
            echo "  --force: Force removal of containers/images."
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
    shift
done

display_whimsical_message

# Determine current time for comparison
# Mock rationale: Allow overriding current date for deterministic testing.
if [[ -n "${TEST_CURRENT_DATE_OVERRIDE:-}" ]]; then
    CURRENT_DATE_ISO="$TEST_CURRENT_DATE_OVERRIDE"
else
    CURRENT_DATE_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)
fi

# Calculate threshold timestamp
# Using GNU date's --date option, which is available in Ubuntu.
THRESHOLD_TIMESTAMP=$(date -u +%s --date="$CURRENT_DATE_ISO - $DAYS_OLD days")

echo "🧹 Initiating temporal cleanup for items older than $DAYS_OLD days (before $(date -u +%Y-%m-%d %H:%M:%S --date="@$THRESHOLD_TIMESTAMP"))."
if "$DRY_RUN"; then
    echo "✨ This is a dry run. No actual resources will be removed."
fi

# --- Clean up exited containers ---
echo "⏳ Scanning for exited containers from forgotten timelines..."
EXPIRED_CONTAINER_IDS=()
# Mock rationale: docker ps output is mocked in tests.
CONTAINER_IDS=$(docker ps -a --filter "status=exited" -q || true) # || true to prevent script from exiting if no containers

if [[ -z "$CONTAINER_IDS" ]]; then
    echo "✨ No exited containers found. The past is clear!"
else
    for CONTAINER_ID in $CONTAINER_IDS; do
        # Mock rationale: docker inspect output is mocked in tests.
        # Using grep -oP for PCRE to extract FinishedAt value from JSON.
        FINISHED_AT_ISO=$(docker inspect "$CONTAINER_ID" | grep -oP '"FinishedAt": "\K[^"]+')
        
        # Convert FinishedAt to Unix timestamp using GNU date.
        FINISHED_TIMESTAMP=$(date -u +%s --date="$FINISHED_AT_ISO")

        if (( FINISHED_TIMESTAMP < THRESHOLD_TIMESTAMP )); then
            EXPIRED_CONTAINER_IDS+=("$CONTAINER_ID")
            echo "  [EXPIRED] Container $CONTAINER_ID (finished at $FINISHED_AT_ISO)"
        else
            echo "  [RECENT] Container $CONTAINER_ID (finished at $FINISHED_AT_ISO)"
        fi
    done

    if [[ ${#EXPIRED_CONTAINER_IDS[@]} -gt 0 ]]; then
        echo "🗑️ Found ${#EXPIRED_CONTAINER_IDS[@]} exited containers to clean."
        if "$DRY_RUN"; then
            echo "  (Dry run) Would remove: ${EXPIRED_CONTAINER_IDS[*]}"
        else
            echo "  Removing exited containers: ${EXPIRED_CONTAINER_IDS[*]}"
            # Mock rationale: docker rm command is mocked in tests.
            docker rm ${FORCE_REMOVE:+"-f"} "${EXPIRED_CONTAINER_IDS[@]}"
            echo "✅ Exited containers removed."
        fi
    else
        echo "✨ No exited containers older than $DAYS_OLD days found. All clear!"
    fi
fi

# --- Clean up dangling images ---
echo "🖼️ Scanning for dangling images, echoes of forgotten builds..."
# Mock rationale: docker images output is mocked in tests.
DANGLING_IMAGE_IDS=$(docker images -f "dangling=true" -q || true) # || true to prevent script from exiting if no images

if [[ -z "$DANGLING_IMAGE_IDS" ]]; then
    echo "✨ No dangling images found. The image registry is pristine!"
else
    echo "🗑️ Found ${#DANGLING_IMAGE_IDS[@]} dangling images to clean."
    if "$DRY_RUN"; then
        echo "  (Dry run) Would remove: ${DANGLING_IMAGE_IDS[*]}"
    else
        echo "  Removing dangling images: ${DANGLING_IMAGE_IDS[*]}"
        # Mock rationale: docker rmi command is mocked in tests.
        docker rmi ${FORCE_REMOVE:+"-f"} "${DANGLING_IMAGE_IDS[@]}"
        echo "✅ Dangling images removed."
    fi
fi

echo "✨ Temporal cleanup complete. The timelines are tidier!"
