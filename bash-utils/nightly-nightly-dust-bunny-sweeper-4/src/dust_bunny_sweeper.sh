#!/bin/bash

# Nightly Dust Bunny Sweeper
# Sweeps away old, forgotten temporary files and empty directories.

# --- Configuration ---
DEFAULT_AGE_DAYS=30 # Default age in days for files/dirs to be considered old

# --- Functions ---

# Display usage information
usage() {
    echo "Usage: $0 <target_directory> [age_in_days] [--dry-run] [--force]"
    echo ""
    echo "  <target_directory> : The path to the directory to sweep."
    echo "  [age_in_days]      : Files and empty directories older than this many days will be swept. Defaults to ${DEFAULT_AGE_DAYS} days."
    echo "  --dry-run          : List what would be swept without actually deleting anything."
    echo "  --force            : Skip confirmation and proceed with deletion immediately. Use with extreme caution."
    echo ""
    echo "Example: $0 /tmp 7 --dry-run"
    echo "Example: $0 ~/downloads 30 --force"
    exit 1
}

# Log messages with a whimsical touch
log_info() {
    echo "✨ $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo "⚠️  $(date '+%Y-%m-%d %H:%M:%S') - WARNING: $1" >&2
}

log_error() {
    echo "❌ $(date '+%Y-%m-%d %H:%M:%S') - ERROR: $1" >&2
    exit 1
}

# --- Main Script ---

TARGET_DIR=""
AGE_DAYS=""
DRY_RUN=0
FORCE=0

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --force)
            FORCE=1
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            elif [[ -z "$AGE_DAYS" && "$1" =~ ^[0-9]+$ ]]; then
                AGE_DAYS="$1"
            else
                log_error "Too many arguments or invalid age: $1"
                usage
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$TARGET_DIR" ]]; then
    log_error "Target directory not specified."
    usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    log_error "Target directory '$TARGET_DIR' does not exist or is not a directory."
fi

if [[ -z "$AGE_DAYS" ]]; then
    AGE_DAYS="${DEFAULT_AGE_DAYS}"
    log_info "No age specified. Defaulting to ${AGE_DAYS} days."
fi

log_info "Initiating Dust Bunny Sweep in '$TARGET_DIR' for items older than ${AGE_DAYS} days."

# Find old files and empty directories
# -type f: regular files
# -type d -empty: empty directories
# -mtime +$AGE_DAYS: modification time older than AGE_DAYS
# -print0: print null-terminated for safety with filenames containing spaces/newlines

log_info "Searching for digital dust bunnies..."

# Find files and empty directories
# We use a single find command targeting files OR empty directories.
# -maxdepth 1 is crucial for safety, only targeting items directly in TARGET_DIR.
OLD_FILES_AND_EMPTY_DIRS=$(find "$TARGET_DIR" -maxdepth 1 \(
    -type f -o \(
        -type d -empty
    \)
\) -mtime +"$AGE_DAYS" -print0)

if [[ -z "$OLD_FILES_AND_EMPTY_DIRS" ]]; then
    log_info "No digital dust bunnies found older than ${AGE_DAYS} days in '$TARGET_DIR'. Your digital space is sparkling clean! ✨"
    exit 0
fi

log_info "Found the following digital dust bunnies to sweep:"

# Print found items for review
# Using 'xargs -0' to handle null-terminated strings from find
# 'sed' is used here to add a prefix for better readability in output
echo "$OLD_FILES_AND_EMPTY_DIRS" | xargs -0 -I {} echo "  - {}"

if [[ "$DRY_RUN" -eq 1 ]]; then
    log_info "This was a dry run. No dust bunnies were swept. To sweep them for real, remove the --dry-run flag."
    exit 0
fi

if [[ "$FORCE" -eq 0 ]]; then
    read -p "Are you sure you want to sweep these digital dust bunnies? (y/N): " -n 1 -r
    echo # Move to a new line
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        log_info "Sweep cancelled. Digital dust bunnies live to see another day (for now)."
        exit 0
    fi
fi

log_info "Sweeping away digital dust bunnies..."

# Perform deletion
echo "$OLD_FILES_AND_EMPTY_DIRS" | xargs -0 rm -rf

if [[ $? -eq 0 ]]; then
    log_info "Digital dust bunnies successfully swept! Your digital space is now tidier. ✨"
else
    log_error "Failed to sweep some digital dust bunnies. Check permissions or try again."
fi
