#!/bin/bash

# Nightly Docker Dust Sweeper - src/sweep.sh

set -euo pipefail

# --- Whimsical Configuration ---
COLOR_GREEN="\033[0;32m"
COLOR_YELLOW="\033[0;33m"
COLOR_RED="\033[0;31m"
COLOR_BLUE="\033[0;34m"
COLOR_RESET="\033[0m"

EMOJI_SWEEP="🧹"
EMOJI_SPARKLE="✨"
EMOJI_DUST="💨"
EMOJI_INFO="ℹ️"
EMOJI_WARNING="⚠️"
EMOJI_SUCCESS="✅"

# --- Helper Functions ---
log_info() { echo -e "${EMOJI_INFO} ${COLOR_BLUE}$1${COLOR_RESET}"; }
log_success() { echo -e "${EMOJI_SUCCESS} ${COLOR_GREEN}$1${COLOR_RESET}"; }
log_warning() { echo -e "${EMOJI_WARNING} ${COLOR_YELLOW}$1${COLOR_RESET}"; }
log_error() { echo -e "${EMOJI_WARNING} ${COLOR_RED}$1${COLOR_RESET}"; exit 1; }

print_banner() {
    echo -e "\n${COLOR_YELLOW}====================================================${COLOR_RESET}"
    echo -e "${COLOR_YELLOW} ${EMOJI_SWEEP} Nightly Docker Dust Sweeper ${EMOJI_SPARKLE} ${COLOR_RESET}"
    echo -e "${COLOR_YELLOW}====================================================${COLOR_RESET}\n"
}

# --- Main Logic ---
DRY_RUN=false

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h|--help)
            echo "Usage: sweep.sh [--dry-run]"
            echo "  --dry-run: Simulate cleanup without actually removing resources."
            exit 0
            ;;
        *)
            log_error "Unknown argument: $arg. Use --help for usage."
            ;;
    esac
done

print_banner

if ! command -v docker &> /dev/null; then
    log_error "Docker command not found. Please ensure Docker is installed and accessible."
fi

if [ "$DRY_RUN" = true ]; then
    log_info "${EMOJI_DUST} Dry run enabled! I'll just tell you what I *would* sweep away. No actual deletion will occur. ${EMOJI_DUST}"
    log_info "Looking for forgotten digital bits..."
    echo ""

    log_info "  --- Exited Containers ---"
    if ! docker ps -a --filter 'status=exited' --format '{{.ID}}' | grep -q .; then
        log_info "    No exited containers found."
    else
        docker ps -a --filter 'status=exited' --format '{{.ID}}\t{{.Image}}\t{{.Names}}' | while read -r ID IMAGE NAME; do
            log_info "    Container (exited): ${NAME} (${IMAGE})"
        done
    fi

    log_info "  --- Dangling Images ---"
    if ! docker images -f 'dangling=true' --format '{{.ID}}' | grep -q .; then
        log_info "    No dangling images found."
    else
        docker images -f 'dangling=true' --format '{{.ID}}\t{{.Repository}}\t{{.Tag}}' | while read -r ID REPO TAG; do
            log_info "    Dangling Image: ${REPO}:${TAG} (ID: ${ID})"
        done
    fi

    log_info "  --- Dangling Volumes ---"
    if ! docker volume ls -f 'dangling=true' --format '{{.Name}}' | grep -q .; then
        log_info "    No dangling volumes found."
    else
        docker volume ls -f 'dangling=true' --format '{{.Name}}' | while read -r NAME; do
            log_info "    Dangling Volume: ${NAME}"
        done
    fi

    log_info "  --- Potentially Unused Networks ---"
    # Mock rationale: This is a simplified way to find potentially unused networks.
    # A true 'dangling' filter for networks is not directly available like for images/volumes.
    # We're just listing non-default bridge networks here as potential candidates.
    if ! docker network ls --filter 'driver=bridge' --filter 'name!=bridge' --filter 'name!=host' --filter 'name!=none' --format '{{.Name}}' | grep -q .; then
        log_info "    No potentially unused networks found."
    else
        docker network ls --filter 'driver=bridge' --filter 'name!=bridge' --filter 'name!=host' --filter 'name!=none' --format '{{.Name}}' | while read -r NAME; do
            log_info "    Potentially Unused Network: ${NAME}"
        done
    fi
    echo ""
    log_success "${EMOJI_SPARKLE} Dry run complete! Your Docker-verse *could* be tidier. ${EMOJI_SPARKLE}"
else
    log_info "${EMOJI_SWEEP} Sweeping away the digital dust bunnies! This might take a moment... ${EMOJI_SWEEP}"
    log_warning "${EMOJI_WARNING} This will remove all stopped containers, dangling images, unused networks, and unused volumes. Proceeding in 5 seconds..."
    sleep 5

    PRUNE_OUTPUT=$(docker system prune -f --volumes 2>&1)
    PRUNE_EXIT_CODE=$?

    if [ $PRUNE_EXIT_CODE -ne 0 ]; then
        log_error "${EMOJI_WARNING} Oh dear, the dust bunnies put up a fight! Cleanup failed.\n${PRUNE_OUTPUT}"
    fi

    echo "\n${COLOR_BLUE}--- Cleanup Report ---${COLOR_RESET}"
    echo "${PRUNE_OUTPUT}"
    echo "${COLOR_BLUE}----------------------${COLOR_RESET}\n"

    if echo "$PRUNE_OUTPUT" | grep -q "Total reclaimed space"; then
        log_success "${EMOJI_SPARKLE} Your Docker-verse is sparkling clean! Digital dust bunnies vanquished! ${EMOJI_SPARKLE}"
    else
        log_info "${EMOJI_INFO} Looks like your Docker-verse was already quite tidy! Not much dust to sweep. ${EMOJI_INFO}"
    fi
fi

log_info "${EMOJI_INFO} Nightly Docker Dust Sweeper finished its rounds. ${EMOJI_INFO}"
