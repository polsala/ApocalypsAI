#!/bin/bash

# Nightly Digital Detritus Duster
# A whimsical Bash script to find and optionally remove old, forgotten files and empty directories, metaphorically dusting off digital detritus.

# --- Configuration ---
DEFAULT_AGE_DAYS=30
DRY_RUN=false
TARGET_DIR="." # Default to current directory

# --- Helper Functions ---
print_help() {
    echo "Usage: $0 [OPTIONS] [DIRECTORY]"
    echo ""
    echo "Metaphorically dusts off digital detritus by finding and optionally removing old files and empty directories."
    echo ""
    echo "Options:"
    echo "  -a, --age DAYS      Files/directories older than DAYS will be considered (default: $DEFAULT_AGE_DAYS days)."
    echo "  -d, --dry-run       Perform a dry run without actually deleting anything."
    echo "  -h, --help          Display this help message."
    echo ""
    echo "Arguments:"
    echo "  DIRECTORY           The directory to scan (default: current directory)."
    echo ""
    echo "Examples:"
    echo "  $0 -a 60 /var/log"
    echo "  $0 --dry-run ~/Downloads"
    echo "  $0"
}

parse_args() {
    while [[ "$#" -gt 0 ]]; do
        case "$1" in
            -a|--age)
                if [[ -z "$2" || "$2" =~ ^- ]]; then
                    echo "Error: --age requires a numeric argument." >&2
                    exit 1
                fi
                if ! [[ "$2" =~ ^[0-9]+$ ]]; then
                    echo "Error: Age must be a positive integer." >&2
                    exit 1
                fi
                DEFAULT_AGE_DAYS="$2"
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                ;;
            -h|--help)
                print_help
                exit 0
                ;;
            -*)
                echo "Error: Unknown option '$1'" >&2
                print_help
                exit 1
                ;;
            *)
                if [[ -d "$1" ]]; then
                    TARGET_DIR="$1"
                else
                    echo "Error: Directory '$1' not found or is not a directory." >&2
                    exit 1
                fi
                ;;
        esac
        shift
    done
}

# --- Main Logic ---
main() {
    parse_args "$@"

    if [[ ! -d "$TARGET_DIR" ]]; then
        echo "Error: Target directory '$TARGET_DIR' does not exist." >&2
        exit 1
    fi

    echo "🧹 ApocalypsAI Digital Detritus Duster 🧹"
    echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $DEFAULT_AGE_DAYS days..."
    echo ""

    # Find old files and empty directories
    # -type f -mtime +N: files modified more than N days ago
    # -type d -empty -mtime +N: empty directories modified more than N days ago
    # -o: OR operator
    # -print0: print null-terminated names for safety with xargs
    # xargs -0: read null-terminated names
    # sort: for consistent output in tests
    OLD_ITEMS=$(find "$TARGET_DIR" -maxdepth 1 -mindepth 1 \( -type f -mtime +"$DEFAULT_AGE_DAYS" -o -type d -empty -mtime +"$DEFAULT_AGE_DAYS" \) -print0 | xargs -0 -r ls -dt | sort)

    if [[ -z "$OLD_ITEMS" ]]; then
        echo "✨ All clear! No digital dust bunnies found in '$TARGET_DIR' older than $DEFAULT_AGE_DAYS days. Your digital space is sparkling!"
        exit 0
    fi

    echo "Found the following digital dust bunnies:"
    echo "----------------------------------------"
    echo "$OLD_ITEMS"
    echo "----------------------------------------"
    echo ""

    if $DRY_RUN; then
        echo "This was a dry run. No files or directories were actually removed."
        echo "To remove them, run without the --dry-run option."
        exit 0
    fi

    read -p "Do you wish to sweep these digital dust bunnies away? (y/N): " -n 1 -r
    echo "" # Newline after read input

    if [[ "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Sweeping away the digital detritus..."
        # Use find again for deletion, ensuring we only delete what was listed
        # -exec rm -rf {} +: delete files/directories found by find
        # This is safer than piping to rm directly if filenames have spaces/special chars
        find "$TARGET_DIR" -maxdepth 1 -mindepth 1 \( -type f -mtime +"$DEFAULT_AGE_DAYS" -o -type d -empty -mtime +"$DEFAULT_AGE_DAYS" \) -exec rm -rf {} +
        echo "🧹 Digital space tidied! May your bits be ever clean."
        exit 0
    else
        echo "Operation cancelled. The digital dust bunnies live to see another cycle."
        exit 0
    fi
}

main "$@"
