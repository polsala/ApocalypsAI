#!/bin/bash

# Nightly Digital Dust Bunny Sweeper
# Identifies and reports on stale temporary files and old logs.

# Default directories to scan if none are provided
DEFAULT_DIRS=("/tmp" "/var/tmp" "/var/log" "~/.cache")

# Default age threshold for 'dust bunnies' (in days)
DUST_BUNNY_AGE_DAYS=${DUST_BUNNY_AGE_DAYS:-30}

# --- Functions ---

# Function to resolve tilde in paths
resolve_path() {
    local path="$1"
    if [[ "$path" == \~* ]]; then
        echo "${HOME}${path:1}"
    else
        echo "$path"
    fi
}

# Function to find and report dust bunnies in a given directory
scan_directory() {
    local dir_path="$1"
    local resolved_dir=$(resolve_path "$dir_path")

    if [[ ! -d "$resolved_dir" ]]; then
        # echo "Skipping non-existent directory: $dir_path" >&2
        return 0
    fi

    # Find files older than DUST_BUNNY_AGE_DAYS, accessed time
    # -atime +N: file was last accessed N*24 hours ago.
    # -print0: print full file name on stdout, followed by a null character.
    # xargs -0: read items from standard input separated by null characters.
    # du -b: display size in bytes
    # sort -rh: sort by human readable size, reverse order
    # head -n 5: take top 5

    # Use a temporary file for results to avoid issues with pipes and subshells
    local temp_file=$(mktemp)
    find "$resolved_dir" -type f -atime +"$DUST_BUNNY_AGE_DAYS" -print0 2>/dev/null | \
        xargs -0 -r du -b 2>/dev/null | \
        sort -rh > "$temp_file"

    if [[ -s "$temp_file" ]]; then
        cat "$temp_file"
    fi
    rm -f "$temp_file"
}

# --- Main Logic ---

echo "🧹 Scanning for lurking digital dust bunnies...\n"

TARGET_DIRS=("$@")
if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    TARGET_DIRS=("${DEFAULT_DIRS[@]}")
fi

ALL_DUST_BUNNIES_RAW=""
for dir in "${TARGET_DIRS[@]}"; do
    ALL_DUST_BUNNIES_RAW+="$(scan_directory "$dir")\n"
done

# Filter out empty lines and sort again to get overall top files
ALL_DUST_BUNNIES=$(echo -e "$ALL_DUST_BUNNIES_RAW" | grep -v '^$' | sort -rh)

if [ -z "$ALL_DUST_BUNNIES" ]; then
    echo "🎉 No digital dust bunnies found! Your system is sparkling clean! 🎉"
else
    TOTAL_SIZE_BYTES=0
    TOTAL_COUNT=0

    while IFS= read -r line; do
        size_bytes=$(echo "$line" | awk '{print $1}')
        TOTAL_SIZE_BYTES=$((TOTAL_SIZE_BYTES + size_bytes))
        TOTAL_COUNT=$((TOTAL_COUNT + 1))
    done <<< "$ALL_DUST_BUNNIES"

    # Convert total size to human-readable format
    TOTAL_SIZE_HUMAN=$(numfmt --to=iec-i --suffix=B --format="%.1f" "$TOTAL_SIZE_BYTES")

    echo "🔍 Found a colony of ${TOTAL_COUNT} digital dust bunnies, weighing in at ${TOTAL_SIZE_HUMAN}!\n"

    echo "Top 5 chonky dust bunnies:"
    echo "$ALL_DUST_BUNNIES" | head -n 5 | while IFS= read -r line; do
        file_path=$(echo "$line" | awk '{print $2}')
        file_size=$(echo "$line" | awk '{print $1}' | numfmt --to=iec-i --suffix=B --format="%.1f")
        # Get last access time (atime) for whimsical reporting
        # Note: stat output varies by OS. This is a common Linux format.
        # Mock rationale: stat is used to get file access time. In tests, we control the file system.
        LAST_ACCESS_SECONDS=$(stat -c %X "$file_path" 2>/dev/null || echo 0)
        CURRENT_SECONDS=$(date +%s)
        AGE_SECONDS=$((CURRENT_SECONDS - LAST_ACCESS_SECONDS))
        AGE_DAYS=$((AGE_SECONDS / 86400))

        if [ "$LAST_ACCESS_SECONDS" -eq 0 ]; then
            echo "- ${file_size}  ${file_path} (access time unknown)"
        else
            echo "- ${file_size}  ${file_path} (last accessed ${AGE_DAYS} days ago)"
        fi
    done

    echo "\n✨ Your system is looking cleaner, even if it's just a report! ✨"
fi
