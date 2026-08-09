#!/bin/bash

# Nightly Digital Detritus Duster
# A whimsical Bash script to identify and optionally "dust" (move to a quarantine directory)
# old or temporary files in specified locations.

DEFAULT_AGE_DAYS=30
DEFAULT_QUARANTINE_DIR="$HOME/DigitalQuarantineZone"
DRY_RUN=0
AGE_DAYS=$DEFAULT_AGE_DAYS
QUARANTINE_DIR=$DEFAULT_QUARANTINE_DIR
EXCLUDE_PATTERNS=()

# --- Whimsical Messages ---
MSG_HEADER="✨ Nightly Digital Detritus Duster Initiated! ✨"
MSG_NO_DETRITUS="🧹 Your digital space is sparkling clean! No detritus found."
MSG_DRY_RUN_HEADER="🔍 Performing a dry run. No files will be moved, just a peek at the digital dust bunnies:"
MSG_DUSTING_HEADER="💨 Sweeping away digital detritus to the Quarantine Zone..."
MSG_QUARANTINE_CREATED="📦 Digital Quarantine Zone created at: "
MSG_QUARANTINE_EXISTS="📦 Digital Quarantine Zone ready at: "
MSG_FILE_FOUND="  - Found a dusty relic: "
MSG_FILE_MOVED="  - Dusted: "
MSG_FILE_SKIPPED="  - Skipping (excluded): "
MSG_CONFIRM="🧹 Ready to dust these relics? (y/N): "
MSG_ABORTED="🚫 Dusting aborted. Your digital detritus lives another day."
MSG_COMPLETED="✅ Digital dusting complete! Your space feels lighter."

# --- Functions ---

# Display usage information
usage() {
    echo -e "$MSG_HEADER\n"
    echo "Usage: $0 [OPTIONS] <DIRECTORY1> [DIRECTORY2...]"
    echo "A whimsical Bash script to identify and optionally 'dust' (move to a quarantine directory)"
    echo "old or temporary files in specified locations, tidying your digital space."
    echo ""
    echo "Options:"
    echo "  -a <days>    Files older than <days> will be considered detritus. Default: $DEFAULT_AGE_DAYS days."
    echo "  -q <path>    Specify the 'Digital Quarantine Zone' directory. Default: $DEFAULT_QUARANTINE_DIR."
    echo "  -d           Dry run mode. Show what would be dusted without moving files."
    echo "  -e <pattern> Exclude files matching this pattern (e.g., '*.log', 'temp_dir/*'). Can be used multiple times."
    echo "  -h           Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -d -a 60 ~/Downloads"
    echo "  $0 -q /var/digital_compost -a 7 /tmp ~/temp"
    echo "  $0 -a 90 -e \"*.gitkeep\" ~/my_project/dist"
    exit 1
}

# Check if a file matches any exclusion pattern
is_excluded() {
    local file="$1"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        # Use bash's pattern matching for simplicity, or grep -q for regex
        # For glob patterns, we can use case statement or fnmatch if available
        # For this simple script, let's assume basic glob-like patterns for `find -not -path`
        # or direct string matching for simplicity in this bash script.
        # For more robust exclusion, `find`'s `-not -path` or `-not -name` is better.
        # Here, we'll check against the basename for simplicity, or full path if pattern contains '/'
        if [[ "$file" == $pattern ]]; then # Basic glob match
            return 0 # Excluded
        fi
        if [[ "$(basename "$file")" == $pattern ]]; then # Basic glob match on basename
            return 0 # Excluded
        fi
    done
    return 1 # Not excluded
}

# --- Main Script ---

echo -e "$MSG_HEADER"

# Parse arguments
while getopts "a:q:de:h" opt; do
    case "$opt" in
        a) AGE_DAYS="$OPTARG" ;;
        q) QUARANTINE_DIR="$OPTARG" ;;
        d) DRY_RUN=1 ;;
        e) EXCLUDE_PATTERNS+=("$OPTARG") ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND-1))

# Validate age
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -le 0 ]; then
    echo "Error: Age must be a positive integer."
    usage
fi

# Target directories
TARGET_DIRS=("$@")
if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    echo "Error: Please specify at least one directory to dust."
    usage
fi

# Resolve quarantine directory path
QUARANTINE_DIR=$(eval echo "$QUARANTINE_DIR") # Expand ~ if present

# Ensure quarantine directory exists
if [ ! -d "$QUARANTINE_DIR" ]; then
    echo -n "$MSG_QUARANTINE_CREATED"
    mkdir -p "$QUARANTINE_DIR" || { echo "Error: Could not create quarantine directory '$QUARANTINE_DIR'."; exit 1; }
    echo "'$QUARANTINE_DIR'"
else
    echo "$MSG_QUARANTINE_EXISTS'$QUARANTINE_DIR'"
fi

FOUND_FILES=()
echo ""

# Find detritus
for dir in "${TARGET_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Warning: Directory '$dir' not found or not a directory. Skipping."
        continue
    }

    # Build find command with exclusions
    FIND_CMD="find \"$dir\" -maxdepth 1 -type f -mtime +$AGE_DAYS"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        # This is a simplified exclusion. For robust glob/regex, `find`'s `-not -path` or `-not -name`
        # would be better, but requires careful construction to avoid breaking the command.
        # For this utility, we'll filter after `find` for simplicity and testability.
        # Mock rationale: The `find` command itself is mocked in tests to control output.
        # The exclusion logic is handled by `is_excluded` function which is also tested.
        true # Placeholder, actual filtering happens below
    done

    # Execute find and filter
    # Mock rationale: `find` command is mocked in tests to return predictable file lists.
    # This allows testing the script's logic without actual file system interaction.
    while IFS= read -r file; do
        if [ -n "$file" ]; then
            if ! is_excluded "$file"; then
                FOUND_FILES+=("$file")
            else
                echo "$MSG_FILE_SKIPPED'$file'"
            fi
        fi
    done < <(eval "$FIND_CMD") # Use process substitution to read output line by line
done

if [ ${#FOUND_FILES[@]} -eq 0 ]; then
    echo "$MSG_NO_DETRITUS"
    exit 0
fi

echo ""
if [ "$DRY_RUN" -eq 1 ]; then
    echo "$MSG_DRY_RUN_HEADER"
    for file in "${FOUND_FILES[@]}"; do
        echo "$MSG_FILE_FOUND'$file'"
    done
    echo ""
    echo "$MSG_COMPLETED (Dry Run)"
    exit 0
fi

echo "$MSG_DUSTING_HEADER"
for file in "${FOUND_FILES[@]}"; do
    echo "$MSG_FILE_FOUND'$file'"
done

echo ""
# Mock rationale: `read` command is mocked in tests to provide a deterministic 'y' or 'N' input.
# This ensures tests don't hang waiting for user input and produce consistent results.
read -p "$MSG_CONFIRM" -n 1 -r
echo "" # Newline after read input

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    for file in "${FOUND_FILES[@]}"; do
        # Mock rationale: `mv` command is mocked in tests to simulate file movement
        # without altering the actual filesystem. It records calls for verification.
        mv "$file" "$QUARANTINE_DIR/" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "$MSG_FILE_MOVED'$file'"
        else
            echo "Error: Failed to dust '$file'."
        fi
    done
    echo ""
    echo "$MSG_COMPLETED"
else
    echo "$MSG_ABORTED"
fi

exit 0
