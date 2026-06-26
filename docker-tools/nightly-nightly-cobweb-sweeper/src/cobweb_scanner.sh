#!/bin/bash

TARGET_DIR="${1:-/scan_target}"
MAX_FILE_SIZE_MB="${MAX_FILE_SIZE_MB:-10}"
EXCLUDE_PATTERNS="${EXCLUDE_PATTERNS:-}" # Comma-separated glob patterns

echo "--- Nightly Cobweb Sweeper Report ---"
echo "Scanning directory: $TARGET_DIR"
echo "Max file size: $MAX_FILE_SIZE_MB MB"
echo "Exclude patterns: ${EXCLUDE_PATTERNS:-(None)}"
echo "-------------------------------------"
echo ""

# Function to check if a file should be excluded based on glob patterns
should_exclude() {
    local file="$1"
    IFS=',' read -ra patterns <<< "$EXCLUDE_PATTERNS"
    for pattern in "${patterns[@]}"; do
        if [[ -n "$pattern" && "$file" == $pattern ]]; then
            return 0 # Exclude
        fi
    done
    return 1 # Do not exclude
}

# Temporary files
echo "### Temporary & Backup Files ###"
find "$TARGET_DIR" -type f \( -name "*.tmp" -o -name "*.bak" -o -name "*~" -o -name ".#*" \) -print0 | while IFS= read -r -d $'\0' file; do
    if ! should_exclude "$file"; then
        echo "  - TEMP: $file"
    fi
done
echo ""

# Empty files
echo "### Empty Files ###"
find "$TARGET_DIR" -type f -empty -print0 | while IFS= read -r -d $'\0' file; do
    if ! should_exclude "$file"; then
        echo "  - EMPTY: $file"
    fi
done
echo ""

# Empty directories
echo "### Empty Directories ###"
find "$TARGET_DIR" -type d -empty -print0 | while IFS= read -r -d $'\0' dir; do
    # Exclude the target directory itself if it's empty, and also check exclude patterns
    if [[ "$dir" != "$TARGET_DIR" ]] && ! should_exclude "$dir"; then
        echo "  - EMPTY_DIR: $dir"
    fi
done
echo ""

# Large files
echo "### Large Files (>${MAX_FILE_SIZE_MB}MB) ###"
find "$TARGET_DIR" -type f -size +${MAX_FILE_SIZE_MB}M -print0 | while IFS= read -r -d $'\0' file; do
    if ! should_exclude "$file"; then
        SIZE_KB=$(du -k "$file" | cut -f1)
        SIZE_MB=$(echo "scale=2; $SIZE_KB / 1024" | bc)
        echo "  - LARGE: ${file} (${SIZE_MB} MB)"
    fi
done
echo ""

# Potentially sensitive files (common names)
echo "### Potentially Sensitive Files ###"
find "$TARGET_DIR" -type f \( -name ".env" -o -name "id_rsa" -o -name "id_dsa" -o -name "credentials.json" -o -name "config.secret" \) -print0 | while IFS= read -r -d $'\0' file; do
    if ! should_exclude "$file"; then
        echo "  - SENSITIVE: $file"
    fi
done
echo ""

echo "--- Scan Complete ---"
