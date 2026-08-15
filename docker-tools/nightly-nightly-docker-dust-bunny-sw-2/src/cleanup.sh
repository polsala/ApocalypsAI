#!/bin/bash

# Default values
DAYS_OLD=${DAYS_OLD:-7} # Default to 7 days
DRY_RUN=${DRY_RUN:-"false"}
VERBOSE=${VERBOSE:-"false"}

log() {
    if [ "$VERBOSE" = "true" ]; then
        echo "🧹 ApocalypsAI Dust Bunny Sweeper: $1"
    fi
}

execute_command() {
    local cmd="$1"
    log "Preparing to execute: $cmd"
    if [ "$DRY_RUN" = "true" ]; then
        echo "  [DRY RUN] Would execute: $cmd"
    else
        eval "$cmd"
        if [ $? -ne 0 ]; then
            log "Oh dear, a dust bunny resisted! Command failed: $cmd"
        fi
    fi
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --days-old) DAYS_OLD="$2"; shift ;;
        --dry-run) DRY_RUN="true" ;;
        --verbose) VERBOSE="true" ;;
        -h|--help)
            echo "Usage: $0 [--days-old N] [--dry-run] [--verbose]"
            echo "  --days-old N: Prune resources older than N days (default: 7)"
            echo "  --dry-run: Show what would be cleaned without actually doing it"
            echo "  --verbose: Enable verbose logging"
            exit 0
            ;;
        *)
            echo "Unknown parameter: $1"
            echo "Use -h or --help for usage information."
            exit 1
            ;;
    esac
    shift
done

log "Starting the great Docker Dust Bunny Sweep!"
log "Targeting resources older than $DAYS_OLD days."
[ "$DRY_RUN" = "true" ] && log "This is a DRY RUN. No actual cleaning will occur."

# Calculate the 'until' filter for Docker commands
# Docker's 'until' filter expects a timestamp or duration (e.g., 24h, 7d)
# We'll convert DAYS_OLD to a duration string
UNTIL_FILTER="${DAYS_OLD}d"

log "Sweeping stopped containers..."
execute_command "docker container prune -f --filter \"until=${UNTIL_FILTER}\"

log "Brushing away dangling images..."
execute_command "docker image prune -f --filter \"until=${UNTIL_FILTER}\"

log "Vacuuming unused volumes..."
execute_command "docker volume prune -f --filter \"until=${UNTIL_FILTER}\"

log "Tidying up unused networks..."
execute_command "docker network prune -f --filter \"until=${UNTIL_FILTER}\"

log "The Docker realm is now sparkling clean! Until next time, little dust bunnies..."
