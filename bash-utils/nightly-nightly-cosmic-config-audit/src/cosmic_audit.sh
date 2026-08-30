#!/bin/bash

# Nightly Cosmic Configuration Auditor
# Audits critical system configuration files against a baseline of checksums.

set -euo pipefail

# --- Configuration ---
# These can be overridden by command line arguments
CONFIG_FILE_LIST_PATH=""
BASELINE_DIR=""

# --- Functions ---

# Function to display usage information
usage() {
    echo "Usage: $0 {init|audit} <config_file_list_path> <baseline_directory>"
    echo "  init: Initializes the baseline checksums for the specified files."
    echo "  audit: Audits the current files against the established baseline."
    echo ""
    echo "  <config_file_list_path>: Path to a file listing configuration files (one per line)."
    echo "  <baseline_directory>: Directory to store/read baseline checksums."
    exit 1
}

# Function to initialize the baseline checksums
init_baseline() {
    local config_list_file="$1"
    local baseline_dir="$2"

    if [ ! -f "$config_list_file" ]; then
        echo "Error: Configuration file list not found at '$config_list_file'" >&2
        exit 1
    fi

    mkdir -p "$baseline_dir"
    echo "Initializing baseline in '$baseline_dir' from '$config_list_file'..."

    while IFS= read -r file_path || [ -n "$file_path" ]; do
        if [ -z "$file_path" ]; then
            continue # Skip empty lines
        fi

        if [ ! -f "$file_path" ]; then
            echo "Warning: File '$file_path' not found, skipping." >&2
            continue
        fi

        local file_basename=$(basename "$file_path")
        local baseline_checksum_file="$baseline_dir/${file_basename}.sha256"

        echo -n "Calculating checksum for '$file_path'... "
        sha256sum "$file_path" | awk '{print $1}' > "$baseline_checksum_file"
        echo "Done. Baseline saved to '$baseline_checksum_file'"
    done < "$config_list_file"
    echo "Baseline initialization complete."
}

# Function to audit files against the baseline
audit_files() {
    local config_list_file="$1"
    local baseline_dir="$2"

    if [ ! -f "$config_list_file" ]; then
        echo "Error: Configuration file list not found at '$config_list_file'" >&2
        exit 1
    fi

    if [ ! -d "$baseline_dir" ]; then
        echo "Error: Baseline directory not found at '$baseline_dir'. Please run 'init' first." >&2
        exit 1
    fi

    echo "Auditing files against baseline in '$baseline_dir' from '$config_list_file'..."

    local overall_status=0 # 0 for OK, 1 for CHANGED/NO BASELINE/FILE NOT FOUND

    while IFS= read -r file_path || [ -n "$file_path" ]; do
        if [ -z "$file_path" ]; then
            continue # Skip empty lines
        fi

        echo -n "Auditing '$file_path'... "

        if [ ! -f "$file_path" ]; then
            echo "FILE NOT FOUND (Current system)"
            overall_status=1
            continue
        fi

        local file_basename=$(basename "$file_path")
        local baseline_checksum_file="$baseline_dir/${file_basename}.sha256"

        if [ ! -f "$baseline_checksum_file" ]; then
            echo "NO BASELINE (Run 'init' to create)"
            overall_status=1
            continue
        fi

        local current_checksum=$(sha256sum "$file_path" | awk '{print $1}')
        local baseline_checksum=$(cat "$baseline_checksum_file")

        if [ "$current_checksum" == "$baseline_checksum" ]; then
            echo "OK"
        else
            echo "CHANGED (Current: $current_checksum, Baseline: $baseline_checksum)"
            overall_status=1
        fi
    done < "$config_list_file"
    echo "Audit complete."
    return $overall_status
}

# --- Main Logic ---

if [ "$#" -lt 3 ]; then
    usage
fi

COMMAND="$1"
CONFIG_FILE_LIST_PATH="$2"
BASELINE_DIR="$3"

case "$COMMAND" in
    init)
        init_baseline "$CONFIG_FILE_LIST_PATH" "$BASELINE_DIR"
        ;;
    audit)
        audit_files "$CONFIG_FILE_LIST_PATH" "$BASELINE_DIR"
        ;;
    *)
        usage
        ;;
esac
