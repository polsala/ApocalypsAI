#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Configuration
DEFAULT_AGE_DAYS=7
DRY_RUN_MESSAGE=" (Dry Run)"

# --- Helper Functions ---

# Function to print messages with a whimsical touch
print_whimsical_message() {
    local message="$1"
    echo -e "🧹✨ $message ✨🧹"
}

# Function to display usage information
usage() {
    echo "Usage: $(basename "$0") <path> [--age <days>] [--clean] [--help]"
    echo ""
    echo "Identifies and optionally cleans up old, forgotten files and directories,"
    echo "metaphorically sweeping away digital dust bunnies."
    echo ""
    echo "Arguments:"
    echo "  <path>        The directory to sweep for digital dust bunnies."
    echo "Options:"
    echo "  --age <days>  Files/directories older than this many days will be considered"
    echo "                dust bunnies. Default: ${DEFAULT_AGE_DAYS} days."
    echo "  --clean       Actually remove the identified dust bunnies. Use with caution!"
    echo "                By default, it performs a dry run and only lists them."
    echo "  --help        Display this help message."
    echo ""
    echo "Example:"
    echo "  $(basename "$0") /var/log --age 30"
    echo "  $(basename "$0") ~/Downloads --clean"
    exit 1
}

# --- Main Logic ---

main() {
    local target_path=""
    local age_days="${DEFAULT_AGE_DAYS}"
    local clean_mode=0

    # Parse arguments
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            --age)
                if [[ -z "$2" || "$2" =~ ^-+ ]]; then
                    print_whimsical_message "Error: --age requires a numeric value."
                    usage
                fi
                age_days="$2"
                shift
                ;;
            --clean)
                clean_mode=1
                ;;
            --help)
                usage
                ;;
            -*)
                print_whimsical_message "Error: Unknown option '$1'."
                usage
                ;;
            *)
                if [[ -z "$target_path" ]]; then
                    target_path="$1"
                else
                    print_whimsical_message "Error: Too many paths specified. Only one <path> argument is allowed."
                    usage
                fi
                ;;
        esac
        shift
    done

    if [[ -z "$target_path" ]]; then
        print_whimsical_message "Error: Missing <path> argument."
        usage
    fi

    if [[ ! -d "$target_path" ]]; then
        print_whimsical_message "Error: Target path '$target_path' is not a valid directory."
        exit 1
    fi

    print_whimsical_message "Initiating Digital Dust Bunny Sweep in '$target_path' for items older than ${age_days} days${DRY_RUN_MESSAGE}..."

    local found_files=()
    local found_dirs=()

    # Find old files
    # Mock rationale: `find` is mocked in tests to control filesystem state and ensure determinism.
    mapfile -t found_files < <(find "$target_path" -type f -mtime +"$age_days" 2>/dev/null)

    # Find old directories (empty or not, we consider them dust bunnies if old)
    # Mock rationale: `find` is mocked in tests to control filesystem state and ensure determinism.
    mapfile -t found_dirs < <(find "$target_path" -type d -mtime +"$age_days" 2>/dev/null)

    local total_found=$(( ${#found_files[@]} + ${#found_dirs[@]} ))

    if [[ "$total_found" -eq 0 ]]; then
        print_whimsical_message "Hooray! No digital dust bunnies found in '$target_path'. Your digital space is sparkling clean!"
        exit 0
    fi

    print_whimsical_message "Found ${total_found} digital dust bunnies:"

    if [[ ${#found_files[@]} -gt 0 ]]; then
        echo "--- Old Files ---"
        for file in "${found_files[@]}"; do
            echo "  - File: $file"
        done
    fi

    if [[ ${#found_dirs[@]} -gt 0 ]]; then
        echo "--- Old Directories ---"
        for dir in "${found_dirs[@]}"; do
            echo "  - Dir: $dir"
        done
    fi

    if [[ "$clean_mode" -eq 1 ]]; then
        print_whimsical_message "Sweeping away the digital dust bunnies..."
        local cleaned_count=0
        for item in "${found_files[@]}" "${found_dirs[@]}"; do
            # Mock rationale: `rm` is mocked in tests to prevent actual filesystem modification and ensure determinism.
            if rm -rf "$item" 2>/dev/null; then
                echo "  🧹 Removed: $item"
                ((cleaned_count++))
            else
                echo "  ⚠️ Failed to remove: $item"
            fi
        done
        print_whimsical_message "Finished sweeping! ${cleaned_count} dust bunnies banished from your system."
    else
        print_whimsical_message "To actually clean these up, run with the '--clean' option."
        print_whimsical_message "Remember, a clean system is a happy system! But always double-check before cleaning."
    fi
}

# Call the main function
main "$@"
