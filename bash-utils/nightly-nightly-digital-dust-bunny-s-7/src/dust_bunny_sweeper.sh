#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default directories to scan for digital dust bunnies (old files)
DEFAULT_SCAN_PATHS=(
    "$HOME/Downloads"
    "$HOME/.cache"
    "/tmp"
    "/var/log"
)

# Default age threshold for files (in days)
DEFAULT_AGE_DAYS=30

# --- Helper Functions ---

# Function to display usage information
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "A whimsical Bash script to find and sweep away digital dust bunnies (old, unused files) from your system."
    echo ""
    echo "Options:"
    echo "  -p, --path <DIR>    Add a directory to scan. Can be used multiple times."
    echo "                      (Defaults: $HOME/Downloads, $HOME/.cache, /tmp, /var/log)"
    echo "  -a, --age <DAYS>    Files older than <DAYS> will be considered dust bunnies. (Default: $DEFAULT_AGE_DAYS days)"
    echo "  -n, --dry-run       Only show what would be swept, do not delete anything."
    echo "  -y, --yes           Assume 'yes' to all prompts and proceed with sweeping."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0"
    echo "  $0 -p /var/tmp -a 60"
    echo "  $0 --dry-run"
}

# Function to check if a directory exists and is readable
is_valid_dir() {
    local dir="$1"
    if [[ -d "$dir" && -r "$dir" ]]; then
        return 0 # True
    else
        echo "Warning: Directory '$dir' does not exist or is not readable. Skipping." >&2
        return 1 # False
    fi
}

# --- Main Logic ---

SCAN_PATHS=()
AGE_DAYS=$DEFAULT_AGE_DAYS
DRY_RUN=false
ASSUME_YES=false

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -p|--path)
            if [[ -n "$2" && "$2" != -* ]]; then
                SCAN_PATHS+=("$2")
                shift
            else
                echo "Error: Argument for $1 is missing." >&2
                show_help
                exit 1
            fi
            ;;n        -a|--age)
            if [[ -n "$2" && "$2" =~ ^[0-9]+$ ]]; then
                AGE_DAYS="$2"
                shift
            else
                echo "Error: Argument for $1 must be a positive number." >&2
                show_help
                exit 1
            fi
            ;;n        -n|--dry-run)
            DRY_RUN=true
            ;;
        -y|--yes)
            ASSUME_YES=true
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'" >&2
            show_help
            exit 1
            ;;
    esac
    shift
done

# If no specific paths were provided, use defaults
if [[ ${#SCAN_PATHS[@]} -eq 0 ]]; then
    SCAN_PATHS=("${DEFAULT_SCAN_PATHS[@]}")
fi

echo "🧹 Nightly Digital Dust Bunny Sweeper 🧹"
echo "---------------------------------------"
echo "Scanning for files older than $AGE_DAYS days in:"
for path in "${SCAN_PATHS[@]}"; do
    echo "  - $path"
done
echo ""

DUST_BUNNIES=()
TOTAL_SIZE_BYTES=0

# Find dust bunnies
for path in "${SCAN_PATHS[@]}"; do
    if is_valid_dir "$path"; then
        # Mock rationale: In tests, 'find' will be mocked to output specific paths.
        # This avoids actual filesystem traversal during testing.
        # The -print0 and xargs -0 are for handling filenames with spaces/special characters.
        # The '|| true' prevents xargs from exiting if 'find' finds nothing.
        while IFS= read -r -d $'\0' file; do
            DUST_BUNNIES+=("$file")
        done < <(find "$path" -type f -atime +"$AGE_DAYS" -print0 2>/dev/null)
    fi
done

if [[ ${#DUST_BUNNIES[@]} -eq 0 ]]; then
    echo "✨ All clear! No digital dust bunnies found. Your system is sparkling clean! ✨"
    exit 0
fi

echo "Found ${#DUST_BUNNIES[@]} digital dust bunnies!"
echo "Calculating their fluffiness (total size)..."

# Calculate total size
# Mock rationale: In tests, 'du' will be mocked to output a specific size.
# This avoids actual disk usage calculation during testing.
# Using 'printf "%s\0"' and 'xargs -0' to handle filenames with spaces/special characters.
# 'du -ch' gives human-readable total.
TOTAL_SIZE_HUMAN=$(printf "%s\0" "${DUST_BUNNIES[@]}" | xargs -0 du -ch 2>/dev/null | tail -n 1 | awk '{print $1}')
# Fallback if du fails or finds nothing
if [[ -z "$TOTAL_SIZE_HUMAN" || "$TOTAL_SIZE_HUMAN" == "0" || "$TOTAL_SIZE_HUMAN" == "0B" ]]; then
    TOTAL_SIZE_HUMAN="unknown size"
fi

echo "Total fluffiness: $TOTAL_SIZE_HUMAN"
echo ""

if $DRY_RUN; then
    echo "--- Dry Run Mode ---"
    echo "The following files would be swept away:"
    for bunny in "${DUST_BUNNIES[@]}"; do
        echo "  - $bunny"
    done
    echo ""
    echo "No files were deleted because you are in dry-run mode."
    exit 0
fi

if ! $ASSUME_YES; then
    read -p "Ready to sweep these digital dust bunnies away? (y/N): " -n 1 -r
    echo ""
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Phew! Operation cancelled. The dust bunnies live to see another day... for now."
        exit 0
    fi
fi

echo "Sweeping away ${#DUST_BUNNIES[@]} digital dust bunnies..."

DELETED_COUNT=0
for bunny in "${DUST_BUNNIES[@]}"; do
    # Mock rationale: In tests, 'rm' will be mocked to prevent actual deletion.
    # It will instead log the attempted deletion or simulate success.
    if rm -f "$bunny" 2>/dev/null; then
        echo "  [SWEPT] $bunny"
        ((DELETED_COUNT++))
    else
        echo "  [FAILED] Could not sweep $bunny" >&2
    fi
done

echo ""
echo "---------------------------------------"
echo "🧹 Sweep complete! $DELETED_COUNT digital dust bunnies have been swept away. 🧹"
echo "Your system feels lighter already!"
