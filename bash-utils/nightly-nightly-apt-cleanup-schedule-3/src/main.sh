#!/usr/bin/env bash
set -euo pipefail

# nightly-apt-cleanup-scheduler.sh
# Whimsical apt cache cleaner with apocalypse warnings.

# Allow overriding the cache directory for testing
APTCACHE_DIR="${APTCACHE_DIR:-/var/cache/apt/archives}"
CRON_SCHEDULE="42 2 * * * $(realpath "$0") --dry-run"
CRON_COMMENT="# nightly-apt-cleanup-scheduler"

APOCALYPSE_QUOTES=(
    "The sky cracks, but your disk stays clean."
    "Even the end of the world needs space."
    "Dust to dust, cache to empty."
    "When the servers fall, your apt cache shall not."
)

function random_quote() {
    echo "${APOCALYPSE_QUOTES[RANDOM % ${#APOCALYPSE_QUOTES[@]}]}"
}

function list_old_packages() {
    find "$APTCACHE_DIR" -type f -mtime +7 -printf "%f\n" || true
}

function clean_cache() {
    sudo apt-get clean -y
}

function install_cron() {
    (crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $CRON_COMMENT") | crontab -
    echo "Cron job installed."
}

function remove_cron() {
    crontab -l 2>/dev/null | grep -v "$CRON_COMMENT" | crontab -
    echo "Cron job removed."
}

DRY_RUN=false
INSTALL_CRON=false
REMOVE_CRON=false

while (( "$#" )); do
    case "$1" in
        --dry-run) DRY_RUN=true ;;
        --install-cron) INSTALL_CRON=true ;;
        --remove-cron) REMOVE_CRON=true ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
    shift
done

if $REMOVE_CRON; then
    remove_cron
    exit 0
fi

if $INSTALL_CRON; then
    install_cron
    exit 0
fi

echo "$(random_quote)"
echo "Scanning for packages older than 7 days in $APTCACHE_DIR ..."
OLD_PACKAGES=$(list_old_packages)

if [[ -z "$OLD_PACKAGES" ]]; then
    echo "No old packages found. Your system is already apocalypse‑ready."
else
    echo "Found old packages:"
    echo "$OLD_PACKAGES"
    if $DRY_RUN; then
        echo "Dry run enabled – not removing anything."
    else
        echo "Cleaning apt cache..."
        clean_cache
        echo "Apt cache cleaned."
    fi
fi

echo "$(random_quote)"
