#!/bin/bash

# Nightly Digital Dust Sweeper
# Sweeps away old, unused files (digital dust) from specified directories.

# --- Configuration ---
MIN_AGE_DAYS=7 # Minimum age in days for files to be considered for deletion
CRITICAL_DIRS=(
    "/" "/bin" "/boot" "/dev" "/etc" "/lib" "/proc" "/root" "/run" "/sbin" "/sys" "/usr" "/var"
)

# --- Helper Functions ---
display_help() {
    echo "Usage: $0 [OPTIONS] <directory> <age_in_days>"
    echo ""
    echo "A bash utility to sweep away digital dust (old, unused files) from specified directories."
    echo "Offers a dry-run mode and a safety threshold."
    echo ""
    echo "Arguments:"
    echo "  <directory>    The path to the directory to clean. Cannot be a critical system directory."
    echo "  <age_in_days>  Files older than this many days will be targeted. Must be ${MIN_AGE_DAYS} or greater."
    echo ""
    echo "Options:"
    echo "  --sweep        REQUIRED to actually delete files. Without this, it's a dry run."
    echo "  --help         Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 /home/user/downloads 30             # Dry run: list files in downloads older than 30 days"
    echo "  $0 --sweep /tmp/old_logs 7             # Live sweep: delete files in /tmp/old_logs older than 7 days"
    echo ""
    echo "Safety Precautions:"
    echo "  - Always start with a dry run! Review the output carefully before using --sweep."
    echo "  - Explicitly forbids cleaning critical system directories."
    echo "  - Enforces a minimum age of ${MIN_AGE_DAYS} days."
    echo "  - Only regular files are targeted for deletion, not directories."
    exit 0
}

is_critical_directory() {
    local dir_to_check="$1"
    for critical_dir in "${CRITICAL_DIRS[@]}"; do
        if [[ "$dir_to_check" == "$critical_dir" ]]; then
            return 0 # Is critical
        fi
    done
    return 1 # Not critical
}

# --- Main Logic ---
SWEEP_MODE=0 # 0 for dry run, 1 for live sweep
TARGET_DIR=""
AGE_DAYS=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --sweep)
            SWEEP_MODE=1
            shift
            ;;
        --help)
            display_help
            ;;
        -*)
            echo "Error: Unknown option '$1'" >&2
            display_help
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            elif [[ -z "$AGE_DAYS" ]]; then
                AGE_DAYS="$1"
            else
                echo "Error: Too many arguments." >&2
                display_help
            fi
            shift
            ;;
    esac
done

# Validate arguments
if [[ -z "$TARGET_DIR" || -z "$AGE_DAYS" ]]; then
    echo "Error: Missing <directory> or <age_in_days> argument." >&2
    display_help
fi

if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
    echo "Error: <age_in_days> must be a positive integer." >&2
    exit 1
fi

if (( AGE_DAYS < MIN_AGE_DAYS )); then
    echo "Error: <age_in_days> must be at least ${MIN_AGE_DAYS}." >&2
    exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

# Resolve target directory to its absolute path for robust critical directory check
TARGET_DIR_ABS=$(realpath -q "$TARGET_DIR")
if [[ $? -ne 0 ]]; then
    echo "Error: Could not resolve absolute path for '$TARGET_DIR'." >&2
    exit 1
fi

if is_critical_directory "$TARGET_DIR_ABS"; then
    echo "Error: Cleaning critical system directory '$TARGET_DIR_ABS' is not allowed for safety reasons." >&2
    exit 1
fi

echo "--- Nightly Digital Dust Sweeper ---"
echo "Target Directory: $TARGET_DIR_ABS"
echo "Files older than: $AGE_DAYS days"

if [[ "$SWEEP_MODE" -eq 0 ]]; then
    echo "Mode: DRY RUN (no files will be deleted)"
    echo "Files that WOULD be swept away:"
    # Mock rationale: Using 'find' with '-print0' and 'xargs -0' is a standard, safe way to handle filenames with spaces/special characters.
    # The 'echo' command is used here to simulate the deletion for the dry run, showing what would be removed.
    find "$TARGET_DIR_ABS" -maxdepth 1 -type f -mtime +"$AGE_DAYS" -print0 | xargs -0 -I {} echo "  - {}"
    echo "--- Dry run complete. No files were deleted. ---"
else
    echo "Mode: LIVE SWEEP (files WILL be deleted!)"
    echo "Sweeping away the following digital dust:"
    # Mock rationale: Using 'find' with '-print0' and 'xargs -0' is a standard, safe way to handle filenames with spaces/special characters.
    # The 'rm -v' command is the actual deletion, with '-v' for verbose output.
    find "$TARGET_DIR_ABS" -maxdepth 1 -type f -mtime +"$AGE_DAYS" -print0 | xargs -0 -I {} rm -v "{}"
    echo "--- Live sweep complete. Digital dust has been swept! ---"
fi

exit 0
