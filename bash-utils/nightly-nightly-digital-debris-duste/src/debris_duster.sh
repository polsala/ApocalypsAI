#!/bin/bash

# --- Configuration ---
TARGET_DIR="${1:-.}"
DAYS_OLD="${2:-30}"
MIN_SIZE_KB="${3:-1}" # Minimum size in KB

# --- Functions ---
log_info() {
    echo "✨ Integrator's Log: $*"
}

log_warning() {
    echo "⚠️ Warning: $*" >&2
}

log_error() {
    echo "❌ Error: $*" >&2
    exit 1
}

confirm_action() {
    local prompt="$1"
    while true; do
        echo -n "$prompt (y/n): "
        read -r response # This 'read' can be mocked by the test script
        case "$response" in
            [yY][eE][sS]|[yY]) return 0 ;;
            [nN][oO]|[nN]) return 1 ;;
            *) echo "Invalid input. Please enter 'y' or 'n'." ;;
        esac
    done
}

# --- Main Logic ---
main() {
    if [[ ! -d "$TARGET_DIR" ]]; then
        log_error "Target directory '$TARGET_DIR' does not exist."
    fi

    log_info "Scanning '$TARGET_DIR' for digital debris older than $DAYS_OLD days and larger than ${MIN_SIZE_KB}KB..."

    # Find files:
    # -type f: regular files
    # -mtime +$DAYS_OLD: modified more than $DAYS_OLD days ago
    # -size +${MIN_SIZE_KB}k: size greater than $MIN_SIZE_KB kilobytes
    # -print0: null-terminated output for safety with filenames containing spaces/newlines
    found_files=$(find "$TARGET_DIR" -type f -mtime +"$DAYS_OLD" -size "+${MIN_SIZE_KB}k" -print0)

    if [[ -z "$found_files" ]]; then
        log_info "No significant digital debris found. Your digital wasteland is surprisingly clean!"
        return 0
    fi

    log_info "Identified the following digital debris:"
    echo -e "$found_files" | xargs -0 -I {} echo "  - {}"

    if confirm_action "Do you wish to scavenge (delete) this digital debris?"; then
        log_info "Initiating debris scavenging..."
        echo -e "$found_files" | xargs -0 rm -v # This 'rm' can be mocked by the test script
        log_info "Digital debris scavenged. The wasteland is a bit tidier."
    else
        log_info "Digital debris left untouched. Perhaps it holds sentimental value."
    fi
}

# Execute main function if script is not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
