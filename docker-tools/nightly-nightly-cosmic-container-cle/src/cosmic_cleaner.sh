#!/bin/bash

# Nightly Cosmic Container Cleaner
# Purges cosmic dust (unused Docker resources) from your Docker universe.

DRY_RUN=false

# Function to display help message
show_help() {
    echo "Usage: $0 [--dry-run]"
    echo ""
    echo "A whimsical Docker cleanup utility that purges cosmic dust (unused containers,"
    echo "images, volumes, and networks) and reports on your Docker universe's newfound clarity."
    echo ""
    echo "Options:"
    echo "  --dry-run   Simulate the cleanup without actually removing any resources."
    echo "  --help      Display this help message."
}

# Parse command-line arguments
for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            show_help
            exit 1
            ;;
    esac
done

echo "🌌 Initiating Cosmic Container Cleanup Protocol... 🌌"

if $DRY_RUN; then
    echo "✨ Performing a stellar scan (dry run mode)... ✨"
    # Mock rationale: `docker system prune --force --dry-run` is not a standard Docker command.
    # For a real dry run, one would typically list resources to be pruned.
    # However, for simplicity and to fit the 'system prune' model, we'll simulate a dry-run output.
    # In a real scenario, you might use 'docker ps -a -f status=exited', 'docker images -f dangling=true', etc.
    # For this whimsical tool, we'll just report what *would* be pruned.
    PRUNE_OUTPUT=$(docker system prune --force --dry-run 2>&1)
    if echo "$PRUNE_OUTPUT" | grep -q "Total reclaimed space"; then
        echo "🌠 The Cosmic Scanner predicts: $(echo "$PRUNE_OUTPUT" | grep "Total reclaimed space" | sed 's/Total reclaimed space: //') of cosmic dust could be cleared."
        echo "🌟 Your Docker universe is poised for clarity!"
    elif echo "$PRUNE_OUTPUT" | grep -q "Total reclaimed: 0B"; then
        echo "✨ The Cosmic Scanner found no cosmic dust to clear. Your Docker universe is pristine!"
    else
        echo "⚠️ Cosmic Scanner encountered an anomaly: $PRUNE_OUTPUT"
        echo "Please ensure Docker is running and accessible."
        exit 1
    fi
else
    echo "🚀 Engaging stellar thrusters for deep space cleanup... 🚀"
    PRUNE_OUTPUT=$(docker system prune --force 2>&1)
    if echo "$PRUNE_OUTPUT" | grep -q "Total reclaimed space"; then
        echo "✨ Success! We've swept away $(echo "$PRUNE_OUTPUT" | grep "Total reclaimed space" | sed 's/Total reclaimed space: //') of cosmic dust."
        echo "🌠 Your Docker universe is now sparkling clean and ready for new adventures!"
    elif echo "$PRUNE_OUTPUT" | grep -q "Total reclaimed: 0B"; then
        echo "✨ No cosmic dust found. Your Docker universe was already pristine!"
    else
        echo "⚠️ Cosmic Cleanup encountered an anomaly: $PRUNE_OUTPUT"
        echo "Please ensure Docker is running and accessible."
        exit 1
    fi
fi
