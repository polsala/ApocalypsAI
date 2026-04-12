#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# A whimsical Bash script to find old, unused files and directories.

# Default values
SCAN_PATH="."
AGE_DAYS=90
EXCLUDE_PATTERNS=(".git" "node_modules" "__pycache__" "target" "build" "dist" "venv" "env" "tmp" "temp" "log" "logs" "cache" "caches" "vendor" "coverage" "report" "reports" "*.log" "*.tmp" "*.bak" "*.swp" "*.swo")
SUGGEST_COMMANDS=false

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo "A whimsical Bash script that identifies old, unused files and directories."
    echo ""
    echo "Options:"
    echo "  -p, --path <directory>     The starting directory to scan. Defaults to '$SCAN_PATH'."
    echo "  -a, --age-days <days>      The minimum age in days for an item to be considered old. Defaults to '$AGE_DAYS'."
    echo "  -e, --exclude <pattern>    A comma-separated list of patterns to exclude. Can be used multiple times."
    echo "                             Defaults to: ${EXCLUDE_PATTERNS[*]}"
    echo "  -s, --suggest-commands     Suggest 'rm' commands for identified items. Use with caution!"
    echo "  -h, --help                 Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") --age-days 180"
    echo "  $(basename "$0") --path ~/my_project --exclude build,dist"
    echo "  $(basename "$0") --suggest-commands"
    exit 0
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--path)
        SCAN_PATH="$2"
        shift # past argument
        shift # past value
        ;;
        -a|--age-days)
        AGE_DAYS="$2"
        # Basic validation for age-days
        if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
            echo "Error: --age-days must be a positive integer." >&2
            exit 1
        fi
        shift # past argument
        shift # past value
        ;;
        -e|--exclude)
        IFS=',' read -r -a NEW_EXCLUDES <<< "$2"
        EXCLUDE_PATTERNS+=("${NEW_EXCLUDES[@]}")
        shift # past argument
        shift # past value
        ;;
        -s|--suggest-commands)
        SUGGEST_COMMANDS=true
        shift # past argument
        ;;
        -h|--help)
        show_help
        ;;
        *)
        echo "Unknown option: $1" >&2
        show_help
        ;;
    esac
done

# Validate scan path
if [[ ! -d "$SCAN_PATH" ]]; then
    echo "Error: Scan path '$SCAN_PATH' is not a valid directory." >&2
    exit 1
fi

# Construct find command exclusions
FIND_EXCLUDE_ARGS=()
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    FIND_EXCLUDE_ARGS+=("-not" "-path" "*/$pattern/*")
    FIND_EXCLUDE_ARGS+=("-not" "-name" "$pattern")
done

# Add common system path exclusions to avoid scanning critical areas
# These are hardcoded for safety and performance.
SYSTEM_EXCLUDES=("/proc" "/sys" "/dev" "/run" "/mnt" "/media" "/var/lib" "/var/cache" "/var/log" "/usr" "/bin" "/sbin" "/lib" "/lib64" "/opt" "/boot")
for sys_path in "${SYSTEM_EXCLUDES[@]}"; do
    FIND_EXCLUDE_ARGS+=("-not" "-path" "${sys_path}/*")
done

echo "🧹 Initiating Digital Dust Bunny Sweep in '$SCAN_PATH' for items older than $AGE_DAYS days..."
echo "--------------------------------------------------------------------------------"

# Find old files and directories
# -mtime +N: File's data was last modified N*24 hours ago.
# -atime +N: File was last accessed N*24 hours ago.
# Using -mtime for modification time, which is generally more indicative of 'unused'.
# -type f: files, -type d: directories

# Find files (Digital Dust Bunnies)
OLD_FILES=$(find "$SCAN_PATH" -xdev -type f -mtime +"$AGE_DAYS" "${FIND_EXCLUDE_ARGS[@]}" 2>/dev/null)

# Find directories (Forgotten Cobwebs)
OLD_DIRS=$(find "$SCAN_PATH" -xdev -type d -mtime +"$AGE_DAYS" "${FIND_EXCLUDE_ARGS[@]}" 2>/dev/null)

FOUND_ANY=false

if [[ -n "$OLD_FILES" ]]; then
    FOUND_ANY=true
    echo "✨ Found some Digital Dust Bunnies (old files):"
    echo "--------------------------------------------------------------------------------"
    while IFS= read -r file; do
        echo "  - File: '$file'"
        if "$SUGGEST_COMMANDS"; then
            echo "    Suggested command: rm -f '$file'"
        fi
    done <<< "$OLD_FILES"
    echo ""
fi

if [[ -n "$OLD_DIRS" ]]; then
    FOUND_ANY=true
    echo "🕸️ Found some Forgotten Cobwebs (old directories):"
    echo "--------------------------------------------------------------------------------"
    while IFS= read -r dir; do
        echo "  - Directory: '$dir'"
        if "$SUGGEST_COMMANDS"; then
            echo "    Suggested command: rm -rf '$dir'"
        fi
    done <<< "$OLD_DIRS"
    echo ""
fi

if ! "$FOUND_ANY"; then
    echo "🎉 Your digital space is sparkling clean! No dust bunnies or cobwebs found."
fi

echo "--------------------------------------------------------------------------------"
echo "🧹 Sweep complete! Remember to review suggested commands carefully before executing them."
