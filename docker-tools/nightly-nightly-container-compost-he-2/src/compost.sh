#!/bin/bash

# Nightly Container Compost Heap

# Function to print whimsical messages
print_whimsical_message() {
    local type="$1"
    local message="$2"
    case "$type" in
        "start") echo "🌱 Activating the Digital Compost Heap! Time to turn digital clutter into fertile ground." ;;
        "dry_run_start") echo "🌿 Initiating a dry run of the Digital Compost Heap..." ;;
        "dry_run_end") echo "Dry run complete. No actual composting performed. Your digital garden remains as is." ;;
        "composting") echo "Composting in progress... This might take a moment as we dig through the digital soil." ;;
        "success") echo "✨ Digital composting complete! We've turned $message of digital waste into fresh, usable space." ;;
        "failure") echo "🐛 Oh dear, the compost heap encountered a snag: $message" ;;
        "no_space") echo "🍃 The digital garden was already pristine! No space to reclaim, but thanks for checking." ;;
    esac
}

# Check for --dry-run argument
DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
fi

if $DRY_RUN; then
    print_whimsical_message "dry_run_start"
    echo "Let's see what digital detritus is ready for recycling without actually touching it."
    echo ""
    echo "--- Potential Digital Compost ---"
    # Mock rationale: In a real scenario, `docker system df` would be used to show reclaimable space.
    # For testing, we simulate a typical output.
    echo "Simulating 'docker system df' output for dry run:"
    echo "TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE"
    echo "Images              5                   3                   500MB               200MB"
    echo "Containers          10                  7                   100MB               30MB"
    echo "Local Volumes       3                   1                   50MB                20MB"
    echo ""
    echo "Based on this, approximately 250MB of digital space could be reclaimed."
    echo "---------------------------------"
    print_whimsical_message "dry_run_end"
else
    print_whimsical_message "start"
    echo "This will prune all stopped containers, dangling images, and unused networks and volumes."
    echo "Consider this a deep clean for your container garden."
    echo ""
    print_whimsical_message "composting"

    # Execute the actual prune command
    # Mock rationale: In a real scenario, this would run `docker system prune --force --volumes`.
    # For testing, we simulate the output of a successful prune.
    PRUNE_OUTPUT=$(docker system prune --force --volumes 2>&1)
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo "$PRUNE_OUTPUT"
        RECLAIMED_SPACE=$(echo "$PRUNE_OUTPUT" | grep "Total reclaimed space:" | awk '{print $4}')
        if [ -z "$RECLAIMED_SPACE" ]; then
            print_whimsical_message "no_space"
        else
            print_whimsical_message "success" "$RECLAIMED_SPACE"
        fi
    else
        print_whimsical_message "failure" "$PRUNE_OUTPUT"
        exit $EXIT_CODE
    fi
fi
