#!/bin/bash

# Default configuration
DEFAULT_PATHS=("/tmp" "/var/tmp" "${HOME}/.cache")
DEFAULT_AGE_DAYS=7
DRY_RUN=true
CONFIRM=true
CLEANUP_EMPTY_DIRS=true

# --- Helper Functions ---

log_info() {
    echo "🧹 INFO: $1"
}

log_warn() {
    echo "⚠️  WARN: $1" >&2
}

log_error() {
    echo "❌ ERROR: $1" >&2
    exit 1
}

usage() {
    echo "Nightly Digital Dust Bunny Sweeper"
    echo "A whimsical utility to find and optionally sweep away old, forgotten 'digital dust bunnies'."
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -p <path>     Specify a directory to scan (can be used multiple times). Defaults to /tmp, /var/tmp, ~/.cache."
    echo "  -a <days>     Files older than <days> will be considered dust bunnies. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  -c            Enable cleanup mode (deletes files/dirs). Requires confirmation unless -f is used."
    echo "  -f            Force cleanup mode without confirmation. Implies -c."
    echo "  -k            Keep empty directories (don't remove them). Default: remove empty directories."
    echo "  -h            Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0                                  # Dry run, default paths, default age"
    echo "  $0 -p /var/log -a 30                # Dry run, scan /var/log, files older than 30 days"
    echo "  $0 -c -p /tmp                       # Cleanup /tmp, default age, with confirmation"
    echo "  $0 -f -p /tmp -a 14                 # Force cleanup /tmp, files older than 14 days"
    echo "  $0 -c -k                            # Cleanup files, but keep empty directories"
    echo ""
}

# --- Main Logic ---

find_dust_bunnies() {
    local target_paths=()
    # Mock rationale: `target_paths` is populated from script arguments or defaults, making it deterministic.
    # The function's behavior is entirely based on these inputs and the test filesystem.
    for p in "$@"; do target_paths+=("$p"); done

    local age_days=$DEFAULT_AGE_DAYS
    if [[ -n "$OPT_AGE_DAYS" ]]; then
        age_days="$OPT_AGE_DAYS"
    fi

    log_info "Scanning for digital dust bunnies older than ${age_days} days in: ${target_paths[*]}"

    for path in "${target_paths[@]}"; do
        if [[ ! -d "$path" ]]; then
            log_warn "Path not found or not a directory, skipping: $path"
            continue
        fi

        # Find old files
        # Mock rationale: `find` is a standard utility and its behavior is deterministic for file system operations.
        # No external services or random elements are involved. The test environment controls the files.
        local files_to_delete=()
        mapfile -t files_to_delete < <(find "$path" -maxdepth 5 -type f -mtime +"$age_days" -print 2>/dev/null)
        if [[ ${#files_to_delete[@]} -gt 0 ]]; then
            log_info "Found ${#files_to_delete[@]} old files in $path:"
            for item in "${files_to_delete[@]}"; do
                log_info "  - $item"
                echo "$item" # Print each item on a new line for mapfile in caller
            done
        fi

        # Find empty directories
        if $CLEANUP_EMPTY_DIRS; then
            # Mock rationale: `find` is a standard utility and its behavior is deterministic for file system operations.
            # No external services or random elements are involved. The test environment controls the directories.
            local empty_dirs=()
            mapfile -t empty_dirs < <(find "$path" -maxdepth 5 -type d -empty -print 2>/dev/null)
            if [[ ${#empty_dirs[@]} -gt 0 ]]; then
                log_info "Found ${#empty_dirs[@]} empty directories in $path:"
                for item in "${empty_dirs[@]}"; do
                    # Exclude the base path itself if it's empty and not explicitly targeted
                    if [[ "$item" != "$path" ]]; then
                        log_info "  - $item (empty directory)"
                        echo "$item" # Print each item on a new line for mapfile in caller
                    fi
                done
            fi
        fi
    done
}

sweep_dust_bunnies() {
    local items_to_sweep=()
    # Mock rationale: `items_to_sweep` is passed directly from the `find_dust_bunnies` function's deterministic output.
    for i in "$@"; do items_to_sweep+=("$i"); done

    if [[ ${#items_to_sweep[@]} -eq 0 ]]; then
        log_info "No dust bunnies found to sweep. Your digital space is sparkling!"
        return 0
    fi

    if $DRY_RUN; then
        log_info "Dry run complete. To sweep these items, run with '-c' or '-f'."
        return 0
    fi

    if $CONFIRM; then
        # Mock rationale: `read` is mocked in tests by piping 'y' to stdin, making user interaction deterministic.
        read -p "Are you sure you want to sweep away ${#items_to_sweep[@]} digital dust bunnies? (y/N): " -n 1 -r
        echo "" # Newline after prompt
        if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
            log_info "Sweep aborted by user."
            return 1
        fi
    fi

    log_info "Sweeping away ${#items_to_sweep[@]} digital dust bunnies..."
    local swept_count=0
    for item in "${items_to_sweep[@]}"; do
        if [[ -e "$item" ]]; then # Check if it still exists before trying to remove
            # Mock rationale: `rm` is a standard utility and its behavior is deterministic for file system operations.
            # It operates on files created and controlled by the test environment.
            if rm -rf "$item"; then
                log_info "  ✅ Swept: $item"
                ((swept_count++))
            else
                log_warn "  ❌ Failed to sweep: $item"
            fi
        else
            log_info "  Skipped (already gone): $item"
        fi
    done
    log_info "Sweep complete. ${swept_count} items removed."
}

main() {
    local custom_paths=()
    local OPT_AGE_DAYS=""

    while getopts "p:a:cfkh" opt; do
        case "$opt" in
            p) custom_paths+=("$OPTARG") ;;
            a) OPT_AGE_DAYS="$OPTARG" ;;
            c) DRY_RUN=false ;;
            f) DRY_RUN=false; CONFIRM=false ;;
            k) CLEANUP_EMPTY_DIRS=false ;;
            h) usage; exit 0 ;;
            *) usage; exit 1 ;;
        esac
    done
    shift $((OPTIND-1))

    local paths_to_scan=("${custom_paths[@]}")
    if [[ ${#paths_to_scan[@]} -eq 0 ]]; then
        # Filter out non-existent default paths
        for p in "${DEFAULT_PATHS[@]}"; do
            if [[ -d "$p" ]]; then
                paths_to_scan+=("$p")
            fi
        done
        # Add Trash directory if it exists
        if [[ -d "${HOME}/.local/share/Trash/files" ]]; then
            paths_to_scan+=("${HOME}/.local/share/Trash/files")
        fi
    fi

    if [[ ${#paths_to_scan[@]} -eq 0 ]]; then
        log_error "No valid paths to scan. Please specify paths with -p or ensure default paths exist."
    fi

    local found_items_output
    # Mock rationale: The output of `find_dust_bunnies` is captured and processed.
    # This internal function call is deterministic and relies only on the test filesystem.
    found_items_output=$(find_dust_bunnies "${paths_to_scan[@]}")
    local found_items_array=()
    mapfile -t found_items_array <<< "$found_items_output"

    sweep_dust_bunnies "${found_items_array[@]}"
}

main "$@"
