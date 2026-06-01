#!/bin/bash

# Nightly PATH Patchwork Organizer
# Cleans, deduplicates, and validates the PATH environment variable.

# --- Configuration ---
# Default action is dry-run
DRY_RUN=true
APPLY_COMMAND=false

# --- Functions ---

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "A whimsical Bash utility to clean, deduplicate, and validate your PATH environment variable."
    echo ""
    echo "Options:"
    echo "  --dry-run   (Default) Shows the proposed cleaned PATH without generating an export command."
    echo "  --apply     Prints the 'export PATH=\"...\"' command to standard output."
    echo "              Use 'eval \"\$($(basename "$0") --apply)\"' to apply changes."
    echo "  --help      Displays this help message."
    echo ""
    echo "Example:"
    echo "  $(basename "$0") --dry-run"
    echo "  eval \"\$($(basename "$0") --apply)\"
}

# Function to clean the PATH
clean_path() {
    local original_path="$1"
    local IFS=':' # Internal Field Separator for splitting PATH
    local -a path_components=($original_path)
    local cleaned_paths=()
    local seen_paths=":" # Initialize with colons to simplify duplicate check regex
    local new_path=""

    for component in "${path_components[@]}"; do
        # Skip empty components
        if [[ -z "$component" ]]; then
            continue
        fi

        # Check if directory exists
        # Mock rationale: In tests, we create dummy directories to simulate existence.
        # In production, this checks actual filesystem.
        if [[ -d "$component" ]]; then
            # Check for duplicates using the :path: pattern
            if [[ ! "$seen_paths" =~ :"$component": ]]; then
                cleaned_paths+=("$component")
                seen_paths="${seen_paths}${component}:"
            fi
        fi
    done

    # Reconstruct the new PATH string
    IFS=':'
    new_path="${cleaned_paths[*]}"
    echo "$new_path"
}

# --- Main Script Logic ---

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            APPLY_COMMAND=false
            ;;
        --apply)
            APPLY_COMMAND=true
            DRY_RUN=false
            ;;
        --help)
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

# Get the current PATH (or a mocked one if set for testing)
CURRENT_PATH="${PATH}"

# Clean the PATH
CLEANED_RESULT=$(clean_path "$CURRENT_PATH")

# Output based on options
if "$APPLY_COMMAND"; then
    echo "export PATH=\"$CLEANED_RESULT\""
else # Default to dry-run
    echo "$CLEANED_RESULT"
fi
