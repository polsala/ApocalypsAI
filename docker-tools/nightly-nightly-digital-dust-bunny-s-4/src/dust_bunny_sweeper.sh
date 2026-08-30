#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Configuration defaults
DRY_RUN="${DRY_RUN:-true}"
MAX_AGE_HOURS="${MAX_AGE_HOURS:-24}"
CLEANUP_IMAGES="${CLEANUP_IMAGES:-true}"
CLEANUP_VOLUMES="${CLEANUP_VOLUMES:-true}"
CLEANUP_NETWORKS="${CLEANUP_NETWORKS:-true}"
CLEANUP_BUILD_CACHE="${CLEANUP_BUILD_CACHE:-true}"

# Determine if it's a dry run
IS_DRY_RUN=false
if [[ "$DRY_RUN" == "true" ]]; then
    IS_DRY_RUN=true
fi

# Whimsical logging function
log_whimsical() {
    local message="$1"
    if $IS_DRY_RUN; then
        echo "    [DRY RUN] $message"
    else
        echo "    $message"
    fi
}

echo "🧹 ApocalypsAI Digital Dust Bunny Sweeper is waking up... 🧹"
if $IS_DRY_RUN; then
    echo "🔍 Scanning for digital dust bunnies (Dry Run mode active!). No actual sweeping will occur."
else
    echo "🚀 Initiating deep clean! Prepare for a sparkling Docker environment."
fi

# --- Image Cleanup ---
if [[ "$CLEANUP_IMAGES" == "true" ]]; then
    echo "⏳ Looking for images older than ${MAX_AGE_HOURS} hours and dangling images..."
    if $IS_DRY_RUN; then
        # Mock rationale: In a real scenario, this would list images. For dry run, we simulate the command.
        # We can't actually get the *number* of images without running docker, so we'll just log the command.
        log_whimsical "Would run: docker image prune --filter \"until=${MAX_AGE_HOURS}h\" --format '{{.ID}} {{.Repository}}:{{.Tag}}'"
        log_whimsical "Would run: docker image prune --filter \"dangling=true\" --format '{{.ID}} {{.Repository}}:{{.Tag}}'"
    else
        # Prune images older than MAX_AGE_HOURS
        echo "      Pruning images older than ${MAX_AGE_HOURS} hours..."
        docker image prune --force --filter "until=${MAX_AGE_HOURS}h"
        # Prune dangling images (not associated with any container)
        echo "      Pruning dangling images..."
        docker image prune --force --filter "dangling=true"
    fi
else
    echo "😴 Skipping image cleanup. Images are allowed to gather dust."
fi

# --- Volume Cleanup ---
if [[ "$CLEANUP_VOLUMES" == "true" ]]; then
    echo "⏳ Looking for unused volumes older than ${MAX_AGE_HOURS} hours..."
    if $IS_DRY_RUN; then
        log_whimsical "Would run: docker volume prune --filter \"until=${MAX_AGE_HOURS}h\" --format '{{.Name}}'"
    else
        docker volume prune --force --filter "until=${MAX_AGE_HOURS}h"
    fi
else
    echo "😴 Skipping volume cleanup. Volumes are cozy in their corners."
fi

# --- Network Cleanup ---
if [[ "$CLEANUP_NETWORKS" == "true" ]]; then
    echo "⏳ Looking for unused networks older than ${MAX_AGE_HOURS} hours..."
    if $IS_DRY_RUN; then
        log_whimsical "Would run: docker network prune --filter \"until=${MAX_AGE_HOURS}h\" --format '{{.Name}}'"
    else
        docker network prune --force --filter "until=${MAX_AGE_HOURS}h"
    fi
else
    echo "😴 Skipping network cleanup. Networks are left to their own devices."
fi

# --- Build Cache Cleanup ---
if [[ "$CLEANUP_BUILD_CACHE" == "true" ]]; then
    echo "⏳ Looking for build cache remnants..."
    if $IS_DRY_RUN; then
        log_whimsical "Would run: docker builder prune --all --filter \"until=${MAX_AGE_HOURS}h\""
    else
        docker builder prune --force --all --filter "until=${MAX_AGE_HOURS}h"
    fi
else
    echo "😴 Skipping build cache cleanup. Some digital cobwebs might remain."
fi

if $IS_DRY_RUN; then
    echo "✨ Dry run complete! Your Docker environment *would* be much tidier. ✨"
    echo "To perform actual cleanup, run with -e DRY_RUN=false."
else
    echo "🎉 Cleanup complete! Your Docker environment is now sparkling clean. 🎉"
fi
