#!/bin/bash

# Nightly Cosmic Dust Collector
# Scans specified directories for stale or empty files, offering to archive or delete them.

set -euo pipefail

# --- Configuration --- #
DEFAULT_AGE_DAYS=30 # Default age for 'stale' files if not specified

# --- Helper Functions --- #
print_help() {
    echo "Usage: $(basename "$0") [OPTIONS] <DIRECTORY>"
    echo "Scans specified directories for stale or empty files, offering to archive or delete them."
    echo ""
    echo "Arguments:"
    echo "  <DIRECTORY>          The path to the directory to scan for cosmic dust."
    echo ""
    echo "Options:"
    echo "  -a, --age <DAYS>     Files older than <DAYS> will be considered cosmic dust."
    echo "                       (e.g., --age 30 for files older than 30 days)."
    echo "  -e, --empty          Include zero-byte files in the cosmic dust collection."
    echo "  -d, --dry-run        (Default) Show what would be done without making any changes."
    echo "  -r, --archive <DIR>  Archive identified files into a tarball in <DIR>."
    echo "                       Files will be removed after successful archiving."
    echo "  -D, --delete         Permanently delete identified files. Use with caution!"
    echo "  -h, --help           Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") --age 90 /var/log                 # Dry run: find files older than 90 days"
    echo "  $(basename "$0") --empty --archive ~/archives ~/downloads # Archive empty files"
    echo "  $(basename "$0") --age 7 --delete /tmp           # DANGEROUS! Delete files older than 7 days"
    exit 0
}

# --- Argument Parsing --- #
TARGET_DIR=""
AGE_DAYS=""
EMPTY_FILES=false
DRY_RUN=true
ARCHIVE_DIR=""
DELETE_FILES=false

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -a|--age)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --age requires a number of days." >&2
                exit 1
            fi
            AGE_DAYS="$2"
            shift # past argument
            shift # past value
            ;;
        -e|--empty)
            EMPTY_FILES=true
            shift # past argument
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift # past argument
            ;;
        -r|--archive)
            if [[ -z "$2" || "$2" =~ ^- ]]; then
                echo "Error: --archive requires an archive directory." >&2
                exit 1
            fi
            ARCHIVE_DIR="$2"
            DRY_RUN=false # Archiving implies action
            shift # past argument
            shift # past value
            ;;
        -D|--delete)
            DELETE_FILES=true
            DRY_RUN=false # Deleting implies action
            shift # past argument
            ;;
        -h|--help)
            print_help
            ;;
        -*)
            echo "Unknown option: $1" >&2
            print_help
            ;;
        *)
            if [[ -z "$TARGET_DIR" ]]; then
                TARGET_DIR="$1"
            else
                echo "Error: Multiple target directories specified or unknown argument: $1" >&2
                print_help
            fi
            shift # past argument
            ;;
    esac
done

# --- Validation --- #
if [[ -z "$TARGET_DIR" ]]; then
    echo "Error: No target directory specified." >&2
    print_help
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

if [[ "$ARCHIVE_DIR" != "" && "$DELETE_FILES" == true ]]; then
    echo "Error: Cannot use --archive and --delete simultaneously." >&2
    exit 1
fi

if [[ "$ARCHIVE_DIR" != "" && ! -d "$ARCHIVE_DIR" ]]; then
    echo "Error: Archive directory '$ARCHIVE_DIR' does not exist or is not a directory." >&2
    exit 1
fi

# --- Build find command --- #
FIND_CMD=("find" "$TARGET_DIR" "-type" "f")

if [[ -n "$AGE_DAYS" ]]; then
    FIND_CMD+=("-mtime" "+"$AGE_DAYS"")
fi

if [[ "$EMPTY_FILES" == true ]]; then
    FIND_CMD+=("-size" "0")
fi

# If no specific criteria (age or empty) are given, default to a reasonable age.
if [[ -z "$AGE_DAYS" && "$EMPTY_FILES" == false ]]; then
    echo "No specific age or empty file criteria provided. Defaulting to files older than ${DEFAULT_AGE_DAYS} days." >&2
    FIND_CMD+=("-mtime" "+"$DEFAULT_AGE_DAYS"")
fi

# --- Execute --- #

# Find the files first
# Using a subshell for the find command to avoid issues with filenames containing spaces/newlines
# and to collect all files before processing.
# Mock rationale: 'find' operates on the local filesystem, which is controlled by the test setup.
readarray -t FILES_TO_PROCESS < <("${FIND_CMD[@]}")

if [[ ${#FILES_TO_PROCESS[@]} -eq 0 ]]; then
    echo "No cosmic dust found in '$TARGET_DIR' matching criteria." >&2
    exit 0
fi

echo "Found ${#FILES_TO_PROCESS[@]} files matching criteria in '$TARGET_DIR'."

if [[ "$DRY_RUN" == true ]]; then
    echo "--- DRY RUN: Files that would be processed ---"
    printf '%s\n' "${FILES_TO_TO_PROCESS[@]}"
    echo "---------------------------------------------"
    echo "Run with --archive <DIR> or --delete to apply changes."
    exit 0
fi

if [[ "$ARCHIVE_DIR" != "" ]]; then
    ARCHIVE_NAME="cosmic_dust_$(date +%Y%m%d%H%M%S).tar.gz"
    ARCHIVE_PATH="$ARCHIVE_DIR/$ARCHIVE_NAME"
    echo "Archiving ${#FILES_TO_PROCESS[@]} files to '$ARCHIVE_PATH'\n"
    # Use tar with -T - to read filenames from stdin, handling spaces/special chars
    # Mock rationale: 'tar' operates on the local filesystem, controlled by the test setup.
    printf '%s\0' "${FILES_TO_PROCESS[@]}" | xargs -0 tar -czf "$ARCHIVE_PATH" -P --null -T - 
    
    if [[ $? -eq 0 ]]; then
        echo "Archive created successfully. Deleting original files..."
        # Mock rationale: 'rm' operates on the local filesystem, controlled by the test setup.
        printf '%s\0' "${FILES_TO_PROCESS[@]}" | xargs -0 rm -f --null -T - 
        if [[ $? -eq 0 ]]; then
            echo "Original files deleted successfully."
        else
            echo "Error: Failed to delete some original files after archiving." >&2
            exit 1
        fi
    else
        echo "Error: Failed to create archive." >&2
        exit 1
    fi
elif [[ "$DELETE_FILES" == true ]]; then
    echo "Deleting ${#FILES_TO_PROCESS[@]} files..."
    # Mock rationale: 'rm' operates on the local filesystem, controlled by the test setup.
    printf '%s\0' "${FILES_TO_PROCESS[@]}" | xargs -0 rm -f --null -T - 
    if [[ $? -eq 0 ]]; then
        echo "Files deleted successfully."
    else
        echo "Error: Failed to delete some files." >&2
        exit 1
    fi
fi

echo "Cosmic dust collection complete."
