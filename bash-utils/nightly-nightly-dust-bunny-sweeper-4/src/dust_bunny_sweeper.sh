#!/bin/bash

# Nightly Dust Bunny Sweeper
# A whimsical Bash script to sweep away digital dust bunnies: old, unused, or broken files and directories.

DEFAULT_AGE_DAYS=30
TARGET_DIR="."
FIND_OLD_FILES=0
FIND_EMPTY_DIRS=0
FIND_BROKEN_LINKS=0
DELETE_MODE=0
INTERACTIVE_MODE=0
AGE_DAYS=$DEFAULT_AGE_DAYS

# --- Helper Functions ---

display_help() {
    echo "Usage: $0 [OPTIONS] [TARGET_DIRECTORY]"
    echo ""
    echo "A whimsical Bash script to sweep away digital dust bunnies: old, unused, or broken files and directories."
    echo ""
    echo "Options:"
    echo "  -a <days>, --age <days>     Find files not accessed in <days> days. Default: $DEFAULT_AGE_DAYS."
    echo "  -e, --empty-dirs            Include empty directories in the scan."
    echo "  -b, --broken-links          Include broken symbolic links in the scan."
    echo "  -d, --delete                Delete found items. Use with extreme caution!"
    echo "  -i, --interactive           Prompt before deleting each item (only with -d)."
    echo "  -h, --help                  Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 -a 60                                 # Dry run, find files older than 60 days in current dir"
    echo "  $0 -e -b /var/log                        # Dry run, find empty dirs and broken links in /var/log"
    echo "  $0 -a 7 -e -b -d -i ~/Downloads          # Delete old files, empty dirs, broken links in ~/Downloads (with prompt)"
    echo "  $0 -a 1 -e -b -d /tmp                    # Automatically delete all findings in /tmp (DANGEROUS!)"
    exit 0
}

log_info() {
    echo "🧹 INFO: $1"
}

log_warning() {
    echo "⚠️  WARNING: $1" >&2
}

log_error() {
    echo "❌ ERROR: $1" >&2
    exit 1
}

# --- Argument Parsing ---

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                log_error "Option -$1 requires an argument (number of days)."
            fi
            AGE_DAYS="$2"
            if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
                log_error "Age must be a positive integer."
            fi
            FIND_OLD_FILES=1
            shift
            ;;
        -e|--empty-dirs)
            FIND_EMPTY_DIRS=1
            ;;
        -b|--broken-links)
            FIND_BROKEN_LINKS=1
            ;;
        -d|--delete)
            DELETE_MODE=1
            ;;
        -i|--interactive)
            INTERACTIVE_MODE=1
            ;;
        -h|--help)
            display_help
            ;;
        -*)
            log_error "Unknown option: $1"
            ;;
        *)
            if [[ -d "$1" ]]; then
                TARGET_DIR="$1"
            else
                log_error "Invalid target directory: $1"
            fi
            ;;
    esac
    shift
done

# If no specific search options are given, default to finding old files
if [[ $FIND_OLD_FILES -eq 0 && $FIND_EMPTY_DIRS -eq 0 && $FIND_BROKEN_LINKS -eq 0 ]]; then
    FIND_OLD_FILES=1
    log_info "No specific search criteria provided. Defaulting to finding files not accessed in $AGE_DAYS days."
fi

# --- Main Logic ---

log_info "Starting digital dust bunny sweep in '$TARGET_DIR'..."
log_info "Mode: $(if [[ $DELETE_MODE -eq 1 ]]; then echo "DELETE"; else echo "DRY RUN"; fi)"

declare -a items_to_clean

# Find old files
if [[ $FIND_OLD_FILES -eq 1 ]]; then
    log_info "Searching for files not accessed in $AGE_DAYS days..."
    # Using -print0 and read -d $'\0' for handling filenames with spaces/special characters
    while IFS= read -r -d $'\0' file; do
        items_to_clean+=("$file")
    done < <(find "$TARGET_DIR" -type f -atime +"$AGE_DAYS" -print0 2>/dev/null)
fi

# Find empty directories
if [[ $FIND_EMPTY_DIRS -eq 1 ]]; then
    log_info "Searching for empty directories..."
    while IFS= read -r -d $'\0' dir; do
        # Exclude the target directory itself if it's empty
        if [[ "$dir" != "$TARGET_DIR" ]]; then
            items_to_clean+=("$dir")
        fi
    done < <(find "$TARGET_DIR" -type d -empty -print0 2>/dev/null)
fi

# Find broken symlinks
if [[ $FIND_BROKEN_LINKS -eq 1 ]]; then
    log_info "Searching for broken symbolic links..."
    while IFS= read -r -d $'\0' link; do
        items_to_clean+=("$link")
    done < <(find "$TARGET_DIR" -xtype l -print0 2>/dev/null)
fi

if [[ ${#items_to_clean[@]} -eq 0 ]]; then
    log_info "No digital dust bunnies found. Your digital space is sparkling clean!"
    exit 0
fi

log_info "Found ${#items_to_clean[@]} digital dust bunnies:"
for item in "${items_to_clean[@]}"; do
    echo "  - $item"
done

if [[ $DELETE_MODE -eq 1 ]]; then
    log_warning "DELETE MODE ACTIVATED! Proceeding with cleanup..."
    for item in "${items_to_clean[@]}"; do
        if [[ $INTERACTIVE_MODE -eq 1 ]]; then
            read -p "Delete '$item'? (y/N) " -n 1 -r
            echo "" # Newline after prompt
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -rf "$item"
                if [[ $? -eq 0 ]]; then
                    log_info "Deleted: $item"
                else
                    log_error "Failed to delete: $item"
                fi
            else
                log_info "Skipped: $item"
            fi
        else
            rm -rf "$item"
            if [[ $? -eq 0 ]]; then
                log_info "Deleted: $item"
            else
                log_error "Failed to delete: $item"
            fi
        fi
    done
    log_info "Cleanup complete."
else
    log_info "Dry run complete. No changes were made. Use -d to delete."
fi
