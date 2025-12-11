#!/bin/bash

# Nightly Digital Detritus Duster
# A whimsical utility to identify and clean up old files and empty directories.

DEFAULT_AGE_DAYS=3
ACTION="report"
SCAN_PATHS=(".")

# --- Helper Functions ---

log_info() { echo -e "\033[0;36m[INFO]\033[0m $1"; }
log_warn() { echo -e "\033[0;33m[WARN]\033[0m $1"; }
log_error() { echo -e "\033[0;31m[ERROR]\033[0m $1"; }
log_success() { echo -e "\033[0;32m[SUCCESS]\033[0m $1"; }

show_usage() {
    echo "Usage: $(basename "$0") [OPTIONS] [PATH...]"
    echo "A whimsical utility to identify and optionally clean up old files and empty directories."
    echo ""
    echo "Options:"
    echo "  -a <days>, --age <days>     Age threshold in days for 'ancient scrolls'. Default: ${DEFAULT_AGE_DAYS}"
    echo "  -q, --quarantine            Move identified detritus to a .digital_detritus_quarantine subdirectory."
    echo "  -d, --delete                Permanently delete identified detritus. USE WITH EXTREME CAUTION!"
    echo "  -h, --help                  Display this help message."
    echo ""
    echo "Arguments:"
    echo "  [PATH...]                   One or more directories to scan. Default: current directory (.)."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -a 5 ."
    echo "  $(basename "$0") -q /var/log /tmp"
    echo "  $(basename "$0") -a 30 -d /home/user/downloads"
    exit 0
}

find_old_files() {
    local path="$1"
    local age_days="$2"
    log_info "Dusting off ancient scrolls in '$path' (older than ${age_days} days)..."
    # Using -mtime +N finds files modified more than N*24 hours ago.
    # -maxdepth 1 to only find files directly in the path, not subdirectories.
    # -print0 for safe handling of filenames with spaces/special chars.
    find "$path" -maxdepth 1 -type f -mtime +"$age_days" -print0
}

find_empty_dirs() {
    local path="$1"
    log_info "Sealing echoing vaults in '$path' (empty directories)..."
    # -mindepth 1 to avoid listing the starting directory itself if it's empty.
    # -empty finds empty files and directories. We filter for directories.
    find "$path" -mindepth 1 -type d -empty -print0
}

perform_action() {
    local item_path="$1"
    local item_type="$2" # 'file' or 'dir'
    local parent_dir
    parent_dir=$(dirname "$item_path")
    local item_name
    item_name=$(basename "$item_path")

    case "$ACTION" in
        "quarantine")
            local quarantine_dir="$parent_dir/.digital_detritus_quarantine"
            mkdir -p "$quarantine_dir" || { log_error "Failed to create quarantine directory: $quarantine_dir"; return 1; }
            if mv "$item_path" "$quarantine_dir/" &>/dev/null; then
                log_success "Quarantined ${item_type} '$item_name' to '$quarantine_dir/'"
            else
                log_warn "Failed to quarantine ${item_type} '$item_name'. It might be in use or permissions issue."
            fi
            ;;
        "delete")
            if rm -rf "$item_path" &>/dev/null; then
                log_success "Purged ${item_type} '$item_name' from existence."
            else
                log_warn "Failed to purge ${item_type} '$item_name'. It might be in use or permissions issue."
            fi
            ;;
        "report")
            log_info "Identified ${item_type}: '$item_path'"
            ;;
    esac
}

# --- Main Logic ---

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--age)
            if [[ -z "$2" || ! "$2" =~ ^[0-9]+$ ]]; then
                log_error "Error: --age requires a positive integer argument."
                show_usage
            fi
            DEFAULT_AGE_DAYS="$2"
            shift # past argument
            shift # past value
            ;;
        -q|--quarantine)
            ACTION="quarantine"
            shift # past argument
            ;;
        -d|--delete)
            ACTION="delete"
            shift # past argument
            ;;
        -h|--help)
            show_usage
            ;;
        -*)
            log_error "Unknown option: $1"
            show_usage
            ;;
        *)
            # Assume paths start here
            if [[ "${#SCAN_PATHS[@]}" -eq 1 && "${SCAN_PATHS[0]}" == "." ]]; then
                SCAN_PATHS=()
            fi
            SCAN_PATHS+=("$1")
            shift # past argument
            ;;
    esac
done

# Validate paths
for path in "${SCAN_PATHS[@]}"; do
    if [[ ! -d "$path" ]]; then
        log_error "Error: Scan path '$path' is not a valid directory."
        exit 1
    fi
done

log_info "Initiating Digital Detritus Duster protocol..."
log_info "Scanning paths: ${SCAN_PATHS[*]}"
log_info "Action: ${ACTION}"

OLD_FILES_FOUND=0
EMPTY_DIRS_FOUND=0

for path in "${SCAN_PATHS[@]}"; do
    # Find old files
    while IFS= read -r -d '' file;
    do
        OLD_FILES_FOUND=$((OLD_FILES_FOUND + 1))
        perform_action "$file" "file"
    done < <(find_old_files "$path" "$DEFAULT_AGE_DAYS")

    # Find empty directories
    while IFS= read -r -d '' dir;
    do
        EMPTY_DIRS_FOUND=$((EMPTY_DIRS_FOUND + 1))
        perform_action "$dir" "dir"
    done < <(find_empty_dirs "$path")
done

log_info "\n--- Detritus Duster Summary ---"
log_info "Ancient Scrolls identified: ${OLD_FILES_FOUND}"
log_info "Echoing Vaults identified: ${EMPTY_DIRS_FOUND}"

if [[ "$OLD_FILES_FOUND" -eq 0 && "$EMPTY_DIRS_FOUND" -eq 0 ]]; then
    log_success "No digital detritus found. Your system is pristine!"
else
    log_warn "Digital detritus detected. Review findings and consider cleanup actions."
fi

exit 0
