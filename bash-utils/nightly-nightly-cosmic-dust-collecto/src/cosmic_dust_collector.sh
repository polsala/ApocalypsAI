#!/bin/bash

# Nightly Cosmic Dust Collector
# A whimsical script to clean up temporary files and old logs,
# reporting the "cosmic dust" collected.

# --- Configuration ---
# Directories to scan for cosmic dust (old files/empty directories)
# Add or remove paths as needed. Be careful with sensitive directories!
declare -a CLEANUP_PATHS=(
    "/tmp"
    "/var/log"
    "${HOME}/.cache"
)

# Files older than this many days will be considered "cosmic dust"
OLD_FILES_DAYS=7

# --- Script Logic ---
DRY_RUN=false
VERBOSE=false
TOTAL_DUST_COLLECTED_BYTES=0

print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "A whimsical script to clean up temporary files and old logs."
    echo ""
    echo "Options:"
    echo "  -d, --dry-run   Perform a dry run without deleting any files."
    echo "  -v, --verbose   Show detailed information about files being processed."
    echo "  -h, --help      Display this help message and exit."
    echo ""
    echo "Configuration can be adjusted within the script itself."
}

parse_args() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                print_help
                exit 1
                ;;
        esac
    done
}

log_message() {
    local level="$1"
    local message="$2"
    if [[ "$VERBOSE" == true || "$level" == "ERROR" || "$level" == "WARN" ]]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $message" >&2
    fi
}

collect_dust_from_path() {
    local path="$1"
    log_message "INFO" "Scanning '$path' for cosmic dust older than ${OLD_FILES_DAYS} days..."

    local files_to_delete=()
    # Find old files
    # Mock rationale: In tests, 'find' is mocked to return predefined paths.
    # In production, it finds actual files.
    mapfile -t files_to_delete < <(find "$path" -type f -mtime +"$OLD_FILES_DAYS" -print 2>/dev/null)

    if [[ ${#files_to_delete[@]} -eq 0 ]]; then
        log_message "INFO" "No ancient cosmic dust found in '$path'."
        return
    fi

    local current_path_dust_bytes=0
    for file in "${files_to_delete[@]}"; do
        if [[ -f "$file" ]]; then
            # Mock rationale: In tests, 'du' is mocked to return a fixed size.
            # In production, it calculates actual file size.
            local file_size_bytes=$(du -b "$file" 2>/dev/null | awk '{print $1}')
            if [[ -n "$file_size_bytes" ]]; then
                current_path_dust_bytes=$((current_path_dust_bytes + file_size_bytes))
            fi

            if [[ "$DRY_RUN" == true ]]; then
                log_message "INFO" "DRY RUN: Would remove ancient cosmic dust: '$file' (Size: $(numfmt --to=iec-i --suffix=B --format='%.1f' "$file_size_bytes"))"
            else
                log_message "INFO" "Removing ancient cosmic dust: '$file' (Size: $(numfmt --to=iec-i --suffix=B --format='%.1f' "$file_size_bytes"))"
                # Mock rationale: In tests, 'rm' is mocked to prevent actual deletion.
                # In production, it performs the deletion.
                rm -f "$file"
                if [[ $? -ne 0 ]]; then
                    log_message "ERROR" "Failed to remove '$file'."
                fi
            fi
        fi
    done

    # Find and remove empty directories
    local empty_dirs=()
    # Mock rationale: In tests, 'find' is mocked to return predefined paths.
    # In production, it finds actual empty directories.
    mapfile -t empty_dirs < <(find "$path" -type d -empty -print 2>/dev/null)

    for dir in "${empty_dirs[@]}"; do
        if [[ "$DRY_RUN" == true ]]; then
            log_message "INFO" "DRY RUN: Would remove empty cosmic void: '$dir'"
        else
            log_message "INFO" "Removing empty cosmic void: '$dir'"
            # Mock rationale: In tests, 'rmdir' is mocked to prevent actual deletion.
            # In production, it performs the deletion.
            rmdir "$dir" 2>/dev/null
            if [[ $? -ne 0 ]]; then
                log_message "ERROR" "Failed to remove empty directory '$dir'."
            fi
        fi
    done

    TOTAL_DUST_COLLECTED_BYTES=$((TOTAL_DUST_COLLECTED_BYTES + current_path_dust_bytes))
}

main() {
    parse_args "$@"

    log_message "INFO" "Initiating Nightly Cosmic Dust Collection..."
    if [[ "$DRY_RUN" == true ]]; then
        log_message "INFO" "--- DRY RUN MODE ACTIVE --- No files will be deleted."
    fi

    for path in "${CLEANUP_PATHS[@]}"; do
        if [[ -d "$path" ]]; then
            collect_dust_from_path "$path"
        else
            log_message "WARN" "Cleanup path '$path' does not exist or is not a directory. Skipping."
        fi
    done

    local total_dust_human_readable=$(numfmt --to=iec-i --suffix=B --format='%.1f' "$TOTAL_DUST_COLLECTED_BYTES")
    log_message "INFO" "Nightly Cosmic Dust Collection complete!"
    log_message "INFO" "Total cosmic dust identified: $total_dust_human_readable"
    if [[ "$DRY_RUN" == true ]]; then
        log_message "INFO" "This was a DRY RUN. No actual dust was removed."
    fi
}

main "$@"
