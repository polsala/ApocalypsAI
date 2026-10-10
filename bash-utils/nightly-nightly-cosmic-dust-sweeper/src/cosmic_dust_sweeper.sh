#!/bin/bash

# Nightly Cosmic Dust Sweeper
# A whimsical yet practical Bash utility to sweep away old log files and temporary data.

# --- Configuration & Defaults ---
TARGET_DIR=""
AGE_DAYS=""
FILE_PATTERN="*"
DRY_RUN=0
VERBOSE=0
EXCLUDE_PATHS=()

# --- Helper Functions ---

# Function to display usage information
usage() {
    echo "Usage: $(basename "$0") -d <directory> -a <age_in_days> [-p <file_pattern>] [-x <exclude_path>] [--dry-run] [--verbose] [--help]"
    echo ""
    echo "Arguments:"
    echo "  -d, --directory <path>   (Required) The target directory to sweep."
    echo "  -a, --age <days>         (Required) Files older than this many days will be considered cosmic dust."
    echo "  -p, --pattern <glob>     (Optional) A file pattern (e.g., '*.log'). Default: '*' (all files)."
    echo "  -x, --exclude <path>     (Optional) A path (file or directory) to exclude. Can be specified multiple times."
    echo "  --dry-run                (Optional) Simulate deletion without actually removing files."
    echo "  --verbose                (Optional) Enable verbose output."
    echo "  -h, --help               (Optional) Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -d /var/log -a 30 --dry-run"
    echo "  $(basename "$0") -d /tmp/my_app -a 7 -p \"*.tmp\""
    exit 1
}

# Function to log messages based on verbosity
log_message() {
    if [[ $VERBOSE -eq 1 ]]; then
        echo "[INFO] $1"
    fi
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -d|--directory)
        TARGET_DIR="$2"
        shift # past argument
        shift # past value
        ;;
        -a|--age)
        AGE_DAYS="$2"
        shift # past argument
        shift # past value
        ;;
        -p|--pattern)
        FILE_PATTERN="$2"
        shift # past argument
        shift # past value
        ;;
        -x|--exclude)
        EXCLUDE_PATHS+=("$2")
        shift # past argument
        shift # past value
        ;;
        --dry-run)
        DRY_RUN=1
        log_message "Dry run mode enabled. No files will be deleted."
        shift # past argument
        ;;
        --verbose)
        VERBOSE=1
        shift # past argument
        ;;
        -h|--help)
        usage
        ;;
        *)
        echo "Error: Unknown option '$1'"
        usage
        ;;
    esac
done

# --- Input Validation ---
if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: Target directory (-d or --directory) is required."
    usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory."
    exit 1
fi

if [[ -z "$AGE_DAYS" ]]; then
    echo "Error: Age in days (-a or --age) is required."
    usage
fi

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: Age in days must be a positive integer."
    exit 1
fi

# --- Construct Find Command ---
FIND_CMD="find \"$TARGET_DIR\" -type f -name \"$FILE_PATTERN\" -mtime +$AGE_DAYS"

for exclude_path in "${EXCLUDE_PATHS[@]}"; do
    FIND_CMD+=" -not -path \"${exclude_path}/*\" -not -name \"$(basename "${exclude_path}")\""
done

# Add print0 for xargs compatibility
FIND_CMD+=" -print0"

log_message "Searching for cosmic dust in '$TARGET_DIR' (older than $AGE_DAYS days, pattern: '$FILE_PATTERN')"
if [[ ${#EXCLUDE_PATHS[@]} -gt 0 ]]; then
    log_message "Excluding paths: ${EXCLUDE_PATHS[*]}"
fi

# --- Execute Sweep ---
if [[ $DRY_RUN -eq 1 ]]; then
    echo "--- DRY RUN: Files that WOULD BE deleted ---"
    eval "$FIND_CMD" | xargs -0 -I {} echo "  [DRY RUN] Would delete: {}"
    echo "--- END DRY RUN ---"
else
    echo "--- Initiating Cosmic Dust Sweep ---"
    if [[ $VERBOSE -eq 1 ]]; then
        eval "$FIND_CMD" | xargs -0 rm -v
    else
        eval "$FIND_CMD" | xargs -0 rm
    fi
    echo "--- Cosmic Dust Sweep Complete ---"
fi

exit 0
