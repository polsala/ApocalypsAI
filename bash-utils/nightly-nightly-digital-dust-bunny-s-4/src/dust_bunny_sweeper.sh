#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# --- Configuration ---
DEFAULT_AGE_DAYS=7
DRY_RUN=false # Set to true for debugging to prevent actual deletion
# --- End Configuration ---

# --- Helper Functions ---
log_info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

log_warn() {
    echo -e "\033[0;33m[WARN]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

show_usage() {
    echo "Usage: $0 <directory_to_scan> <age_in_days> [--force]"
    echo ""
    echo "  <directory_to_scan> : The path to the directory to scan (e.g., /tmp, ~/.cache)."
    echo "  <age_in_days>       : Files and empty directories older than this many days will be considered dust bunnies."
    echo "                        Defaults to $DEFAULT_AGE_DAYS days if not provided or invalid."
    echo "  --force             : (Optional) Skip the confirmation prompt and proceed directly with deletion."
    echo ""
    echo "Example:"
    echo "  $0 /tmp 7"
    echo "  $0 ~/.cache 30 --force"
    exit 1
}

# --- Main Logic ---

# Parse arguments
TARGET_DIR=""
AGE_DAYS=""
FORCE_DELETE=false

if [[ "$#" -lt 1 ]]; then
    show_usage
fi

TARGET_DIR="$1"
if [[ ! -d "$TARGET_DIR" ]]; then
    log_error "Error: Directory '$TARGET_DIR' does not exist or is not a directory."
    show_usage
fi

# Validate age_in_days
if [[ "$#" -ge 2 ]]; then
    if [[ "$2" =~ ^[0-9]+$ ]]; then
        AGE_DAYS="$2"
    elif [[ "$2" == "--force" ]]; then
        FORCE_DELETE=true
    else
        log_warn "Invalid age '$2'. Using default age of $DEFAULT_AGE_DAYS days."
        AGE_DAYS="$DEFAULT_AGE_DAYS"
    fi
fi

if [[ -z "$AGE_DAYS" ]]; then
    AGE_DAYS="$DEFAULT_AGE_DAYS"
fi

# Check for --force in remaining arguments
for arg in "${@:3}"; do
    if [[ "$arg" == "--force" ]]; then
        FORCE_DELETE=true
        break
    fi
done

log_info "Scanning '$TARGET_DIR' for digital dust bunnies older than $AGE_DAYS days..."

# Find old files and empty directories
# -type f -mtime +N: regular files modified N*24 hours ago.
# -type d -empty -mtime +N: empty directories modified N*24 hours ago.
# -print0: print full file name on stdout, followed by a null character. Safer for filenames with spaces/special chars.
DUST_BUNNIES=$(find "$TARGET_DIR" -depth \( -type f -mtime +"$AGE_DAYS" -o -type d -empty -mtime +"$AGE_DAYS" \) -print0 2>/dev/null)

if [[ -z "$DUST_BUNNIES" ]]; then
    log_info "No digital dust bunnies found in '$TARGET_DIR' older than $AGE_DAYS days. Your digital space is sparkling!"
    exit 0
fi

log_info "Found the following digital dust bunnies:"
echo "$DUST_BUNNIES" | xargs -0 -I {} echo "  - {}"

if [[ "$DRY_RUN" == "true" ]]; then
    log_warn "DRY RUN: No files will be deleted."
    exit 0
fi

if [[ "$FORCE_DELETE" == "false" ]]; then
    read -p "Sweep away these digital dust bunnies? (y/N): " -n 1 -r
    echo "" # Newline after prompt
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        log_info "Digital dust bunnies spared. They'll continue to gather..."
        exit 0
    fi
fi

log_info "Sweeping away digital dust bunnies..."

# Delete the identified files and empty directories
# -depth: process directory's contents before the directory itself. Important for -empty.
# -exec rm -rf {} +: execute rm -rf on batches of found items.
# Note: find -empty will find empty files AND empty directories. rm -rf is safe for both.
echo "$DUST_BUNNIES" | xargs -0 rm -rf
# Check if rm command was successful
if [[ "$?" -eq 0 ]]; then
    log_info "Digital dust bunnies successfully swept away!"
else
    log_error "An error occurred during the sweeping process. Some dust bunnies might remain."
    exit 1
fi

exit 0
