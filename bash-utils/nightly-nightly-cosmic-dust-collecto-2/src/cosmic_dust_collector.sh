#!/bin/bash

# Nightly Cosmic Dust Collector
# Sweeps away digital detritus (old files, empty directories) from specified paths.

# --- Configuration ---
DEFAULT_AGE_DAYS=7
DRY_RUN=false
TARGET_DIRS=()
AGE_THRESHOLD=$DEFAULT_AGE_DAYS

# --- Functions ---

# Display usage information
show_help() {
    echo "Usage: $0 [OPTIONS] --target <directory>"
    echo ""
    echo "A whimsical utility to sweep away digital detritus (old files, empty directories)."
    echo ""
    echo "Options:"
    echo "  -t, --target <directory>  Required. The directory path to scan for cosmic dust."
    echo "                            Can be specified multiple times."
    echo "  -a, --age <days>          Collects files and empty directories older than <days> (default: ${DEFAULT_AGE_DAYS} days)."
    echo "  -d, --dry-run             Perform a dry run. Show what *would* be collected without deleting."
    echo "  -h, --help                Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 --dry-run --age 30 --target ~/my_temp_files"
    echo "  $0 --age 14 --target /tmp --target /var/log"
    echo "  $0 --age 0 --target . # Remove all empty directories in current path"
    exit 0
}

# Parse command-line arguments
parse_args() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -t|--target)
                if [[ -z "$2" || "$2" == -* ]]; then
                    echo "Error: --target requires a directory path." >&2
                    exit 1
                fi
                TARGET_DIRS+=("$2")
                shift
                ;;
            -a|--age)
                if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                    echo "Error: --age requires a positive integer for days." >&2
                    exit 1
                fi
                AGE_THRESHOLD="$2"
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                ;;
            -h|--help)
                show_help
                ;;
            *)
                echo "Error: Unknown option '$1'" >&2
                show_help
                ;;
        esac
        shift
    done

    if [[ ${#TARGET_DIRS[@]} -eq 0 ]]; then
        echo "Error: At least one --target directory is required." >&2
        show_help
    fi
}

# Perform the cosmic sweep
perform_sweep() {
    local total_files_collected=0
    local total_dirs_collected=0

    echo "🌌 Initiating Cosmic Dust Collection (Age Threshold: ${AGE_THRESHOLD} days) 🌌"
    [[ "$DRY_RUN" == "true" ]] && echo "--- DRY RUN MODE --- No actual deletions will occur. ---"

    for target_dir in "${TARGET_DIRS[@]}"; do
        if [[ ! -d "$target_dir" ]]; then
            echo "Warning: Target directory '$target_dir' does not exist or is not a directory. Skipping." >&2
            continue
        }

        echo "Scanning '$target_dir' for cosmic dust..."

        # Find and collect old files
        echo "  Searching for ancient stardust (files older than ${AGE_THRESHOLD} days)..."
        local files_to_collect
        # Mock rationale: Using 'find' directly in a controlled temporary directory for tests.
        # This allows testing the actual 'find' behavior without external dependencies.
        files_to_collect=$(find "$target_dir" -type f -mtime +"$AGE_THRESHOLD" -print0 2>/dev/null)
        if [[ -n "$files_to_collect" ]]; then
            echo "$files_to_collect" | while IFS= read -r -d $'\0' file; do
                echo "    [FILE] $(basename "$file") (Path: $file)"
                if [[ "$DRY_RUN" == "false" ]]; then
                    rm -f "$file"
                    if [[ $? -eq 0 ]]; then
                        ((total_files_collected++))
                    else
                        echo "      Failed to remove file: $file" >&2
                    fi
                fi
            done
        else
            echo "    No ancient stardust found."
        fi

        # Find and collect empty directories (process from deepest first)
        echo "  Searching for desolate voids (empty directories)..."
        local dirs_to_collect
        # Mock rationale: Using 'find' directly in a controlled temporary directory for tests.
        # This allows testing the actual 'find' behavior without external dependencies.
        dirs_to_collect=$(find "$target_dir" -depth -type d -empty -print0 2>/dev/null)
        if [[ -n "$dirs_to_collect" ]]; then
            echo "$dirs_to_collect" | while IFS= read -r -d $'\0' dir; do
                # Exclude the target_dir itself if it becomes empty during the process
                if [[ "$dir" == "$target_dir" ]]; then
                    continue
                fi
                echo "    [DIR] $(basename "$dir") (Path: $dir)"
                if [[ "$DRY_RUN" == "false" ]]; then
                    rmdir "$dir" 2>/dev/null # rmdir only removes empty directories
                    if [[ $? -eq 0 ]]; then
                        ((total_dirs_collected++))
                    else
                        echo "      Failed to remove empty directory: $dir" >&2
                    fi
                fi
            done
        else
            echo "    No desolate voids found."
        fi
    done

    echo ""
    echo "--- Cosmic Sweep Report ---"
    echo "Files collected: $total_files_collected"
    echo "Empty directories collected: $total_dirs_collected"
    [[ "$DRY_RUN" == "true" ]] && echo "--- This was a DRY RUN. No actual changes were made. ---"
    echo "🌌 Cosmic Dust Collection Complete! Your digital realm is a bit cleaner. 🌌"
}

# --- Main Execution ---
parse_args "$@"
perform_sweep
