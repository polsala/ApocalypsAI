#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Whimsical-yet-useful utility for the ApocalypsAI community.

# --- Configuration ---
# Directories that should NEVER be touched by the sweeper.
# Add more critical paths as needed.
CRITICAL_PATHS=(
    "/" "/bin" "/boot" "/dev" "/etc" "/lib" "/lib64" "/proc" "/run" "/sbin"
    "/sys" "/usr" "/var/lib" "/var/run" "/var/lock" "/var/spool"
)

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 <directory> <age_in_days> [--dry-run] [--force]"
    echo ""
    echo "  <directory>   : The path to scan for digital dust bunnies."
    echo "  <age_in_days> : Files/directories older than this (in days) will be considered dust bunnies."
    echo "  --dry-run     : Simulate the cleanup without actually deleting anything."
    echo "  --force       : Skip confirmation prompt and proceed with deletion."
    echo ""
    echo "Example: $0 /var/log 30 --dry-run"
    echo "         $0 /tmp 7 --force"
    exit 1
}

is_critical_path() {
    local path="$1"
    for cp in "${CRITICAL_PATHS[@]}"; do
        if [[ "$path" == "$cp" || "$path" == "$cp/" ]]; then
            return 0 # Is a critical path
        fi
    done
    return 1 # Not a critical path
}

# --- Main Logic ---
TARGET_DIR=""
AGE_DAYS=""
DRY_RUN=0
FORCE_DELETE=0

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=1
            shift
            ;;
        --force)
            FORCE_DELETE=1
            shift
            ;;
        -h|--help)
            print_help
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            elif [[ -z "$AGE_DAYS" ]]; then
                AGE_DAYS="$1"
            else
                echo "Error: Unknown argument or too many arguments: $1"
                print_help
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$TARGET_DIR" || -z "$AGE_DAYS" ]]; then
    echo "Error: Missing directory or age_in_days."
    print_help
fi

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [[ "$AGE_DAYS" -lt 0 ]]; then
    echo "Error: Age in days must be a non-negative integer."
    print_help
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

# Check for critical paths
if is_critical_path "$TARGET_DIR"; then
    echo "Warning: Attempting to sweep a critical system path: '$TARGET_DIR'."
    echo "This operation is highly discouraged and could lead to system instability."
    if [[ "$FORCE_DELETE" -eq 0 ]]; then
        read -r -p "Are you absolutely sure you want to proceed? (yes/No): " response
        if ! [[ "$response" =~ ^[Yy][Ee][Ss]$ ]]; then
            echo "Operation cancelled. Better safe than sorry!"
            exit 0
        fi
    fi
    echo "Proceeding with caution..."
fi

echo "--- Nightly Digital Dust Bunny Sweeper ---"
echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $AGE_DAYS days..."

# Find old files and directories, excluding the target directory itself
# -mindepth 1 ensures we don't try to delete the TARGET_DIR itself
# -print0 and xargs -0 handle filenames with spaces/special characters
OLD_ITEMS=$(find "$TARGET_DIR" -mindepth 1 -mtime +"$AGE_DAYS" -print0)

if [[ -z "$OLD_ITEMS" ]]; then
    echo "No digital dust bunnies found. Your system is sparkling clean!"
    exit 0
fi

echo "Found the following digital dust bunnies:"
echo "$OLD_ITEMS" | xargs -0 -I {} echo "  - {}"

if [[ "$DRY_RUN" -eq 1 ]]; then
    echo ""
    echo "--- DRY RUN COMPLETE ---"
    echo "The above items *would have been* swept away. No actual changes made."
    exit 0
fi

if [[ "$FORCE_DELETE" -eq 0 ]]; then
    echo ""
    read -r -p "Proceed with sweeping these digital dust bunnies? (y/N): " response
    if ! [[ "$response" =~ ^[Yy]$ ]]; then
        echo "Sweeping cancelled. The dust bunnies live to see another day!"
        exit 0
    fi
fi

echo "Initiating the sweep... Farewell, digital dust bunnies!"
echo "$OLD_ITEMS" | xargs -0 rm -rf

if [[ "$?" -eq 0 ]]; then
    echo "Sweep complete! Your system breathes a sigh of relief."
else
    echo "Warning: Some dust bunnies might have resisted the sweep. Check logs for errors."
fi

exit 0
