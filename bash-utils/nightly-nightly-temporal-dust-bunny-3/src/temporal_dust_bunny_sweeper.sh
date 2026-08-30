#!/bin/bash

# Nightly Temporal Dust Bunny Sweeper
# Scans specified directories for ancient, forgotten files and directories (temporal dust bunnies)
# older than a configurable threshold, offering to list or sweep them into the void.

# --- Configuration ---
DEFAULT_AGE_DAYS=90
SWEEPER_LOG="/tmp/temporal_dust_bunny_sweeper.log" # Log file for sweep operations

# --- Whimsical Messages ---
MSG_SCANNING="Initiating Temporal Dust Bunny Scan in the designated realms..."
MSG_FOUND_BUNNIES="Behold! Ancient temporal dust bunnies detected:"
MSG_NO_BUNNIES="The temporal realms are surprisingly pristine. No dust bunnies found."
MSG_DRY_RUN="This was a dry run. No temporal matter was disturbed. To sweep, use --sweep or --archive."
MSG_SWEEPING="Commencing temporal sweep! These dust bunnies are returning to the void..."
MSG_ARCHIVING="Relocating temporal dust bunnies to the designated archive realm: "
MSG_COMPLETED="Temporal sweep complete. The realms are a bit tidier now."
MSG_ERROR="Temporal anomaly detected: "

# --- Functions ---

usage() {
    echo "Usage: $0 [OPTIONS] <DIRECTORY...>"
    echo "Scans specified directories for files and directories older than a threshold."
    echo ""
    echo "Options:"
    echo "  -a, --age <DAYS>     Age threshold in days (default: ${DEFAULT_AGE_DAYS})."
    echo "  -d, --dry-run        List temporal dust bunnies without taking action."
    echo "  -s, --sweep          Permanently delete detected temporal dust bunnies."
    echo "  -r, --archive <DIR>  Move detected temporal dust bunnies to an archive directory."
    echo "  -h, --help           Display this help message."
    echo ""
    echo "Example: $0 --age 60 --dry-run /var/log /tmp"
    echo "Example: $0 --age 30 --sweep /old_data"
    echo "Example: $0 --archive /temporal_void /home/user/downloads"
    exit 1
}

log_action() {
    local message="$1"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $message" >> "$SWEEPER_LOG"
}

# --- Main Logic ---

AGE_DAYS=${DEFAULT_AGE_DAYS}
DRY_RUN=true
SWEEP=false
ARCHIVE_DIR=""
TARGET_DIRS=()

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "${MSG_ERROR}Missing age value for --age."
                usage
            fi
            AGE_DAYS="$2"
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            ;;
        -s|--sweep)
            SWEEP=true
            DRY_RUN=false # Sweep implies not dry-run
            ;;
        -r|--archive)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "${MSG_ERROR}Missing archive directory for --archive."
                usage
            fi
            ARCHIVE_DIR="$2"
            DRY_RUN=false # Archive implies not dry-run
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "${MSG_ERROR}Unknown option: $1"
            usage
            ;;
        *)
            TARGET_DIRS+=("$1")
            ;;
    esac
    shift
done

if [[ ${#TARGET_DIRS[@]} -eq 0 ]]; then
    echo "${MSG_ERROR}No target directories specified."
    usage
fi

if [[ "$SWEEP" == "true" && -n "$ARCHIVE_DIR" ]]; then
    echo "${MSG_ERROR}Cannot use --sweep and --archive simultaneously. Choose one."
    usage
fi

if [[ -n "$ARCHIVE_DIR" ]]; then
    if [[ ! -d "$ARCHIVE_DIR" ]]; then
        echo "Creating temporal archive realm: $ARCHIVE_DIR"
        mkdir -p "$ARCHIVE_DIR" || { echo "${MSG_ERROR}Failed to create archive directory: $ARCHIVE_DIR"; exit 1; }
    fi
fi

echo "$MSG_SCANNING"
log_action "$MSG_SCANNING"

FOUND_BUNNIES=0
for dir in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        echo "Warning: Directory not found, skipping: $dir"
        log_action "Warning: Directory not found, skipping: $dir"
        continue
    }

    # Find files and directories older than AGE_DAYS
    # -mtime +N: files modified N*24 hours ago. +90 means more than 90 days.
    # -maxdepth 0: Exclude the starting-point itself from the results.
    # -print0: Null-terminate output for safe processing with xargs.
    # -type f -o -type d: find files OR directories
    # Exclude the archive directory itself if it's within a target dir
    find "$dir" -mindepth 1 -mtime +"$AGE_DAYS" \( -type f -o -type d \) -print0 | while IFS= read -r -d $'\0' item; do
        if [[ -n "$ARCHIVE_DIR" && "$item" == "$ARCHIVE_DIR" ]]; then
            continue # Don't archive the archive directory itself
        fi
        if [[ "$DRY_RUN" == "true" ]]; then
            echo "  - [DRY RUN] Found: $item (modified > ${AGE_DAYS} days ago)"
            FOUND_BUNNIES=$((FOUND_BUNNIES + 1))
        elif [[ "$SWEEP" == "true" ]]; then
            echo "  - Sweeping: $item"
            rm -rf "$item"
            if [[ $? -eq 0 ]]; then
                log_action "Swept: $item"
                FOUND_BUNNIES=$((FOUND_BUNNIES + 1))
            else
                echo "${MSG_ERROR}Failed to sweep: $item"
                log_action "${MSG_ERROR}Failed to sweep: $item"
            fi
        elif [[ -n "$ARCHIVE_DIR" ]]; then
            echo "  - Archiving: $item to $ARCHIVE_DIR"
            mv "$item" "$ARCHIVE_DIR/"
            if [[ $? -eq 0 ]]; then
                log_action "Archived: $item to $ARCHIVE_DIR"
                FOUND_BUNNIES=$((FOUND_BUNNIES + 1))
            else
                echo "${MSG_ERROR}Failed to archive: $item"
                log_action "${MSG_ERROR}Failed to archive: $item"
            fi
        fi
    done
done

if [[ "$FOUND_BUNNIES" -gt 0 ]]; then
    echo "$MSG_FOUND_BUNNIES"
else
    echo "$MSG_NO_BUNNIES"
fi

if [[ "$DRY_RUN" == "true" ]]; then
    echo "$MSG_DRY_RUN"
else
    echo "$MSG_COMPLETED"
fi

log_action "$MSG_COMPLETED"
exit 0
