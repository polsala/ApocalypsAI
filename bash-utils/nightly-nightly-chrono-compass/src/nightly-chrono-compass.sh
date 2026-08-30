#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 [DIRECTORY] [DAYS_AGO] [KEYWORD1 KEYWORD2 ...]"
    echo "  DIRECTORY: The directory to scan (default: current directory)"
    echo "  DAYS_AGO:  Files modified within this many days will be considered 'recent' (default: 1)"
    echo "  KEYWORDS:  Optional keywords to search for within recent files (case-insensitive)"
    echo ""
    echo "Example: $0 /var/log 7 ERROR WARNING"
    exit 1
}

# --- Main Script ---

# Default values
SCAN_DIR="${1:-.}"
DAYS_AGO="${2:-1}"
shift 2 # Shift past directory and days_ago

KEYWORDS=("$@") # Remaining arguments are keywords

if [ ! -d "$SCAN_DIR" ]; then
    echo "Error: Directory '$SCAN_DIR' not found." >&2
    usage
fi

echo "--- Chrono-Compass Temporal Anomaly Report ---"
echo "Scanning directory: '$SCAN_DIR'"
echo "Looking for files modified within the last $DAYS_AGO day(s)."
if [ ${#KEYWORDS[@]} -gt 0 ]; then
    echo "Searching for keywords: '${KEYWORDS[*]}'"
else
    echo "No specific keywords provided."
fi
echo "----------------------------------------------"
echo ""

# Find files modified in the last N days
# -mtime -N: files modified less than N*24 hours ago
# 2>/dev/null suppresses permission denied errors
RECENT_FILES=$(find "$SCAN_DIR" -type f -mtime -"$DAYS_AGO" 2>/dev/null)

if [ -z "$RECENT_FILES" ]; then
    echo "No recent temporal echoes detected in the last $DAYS_AGO day(s)."
else
    echo "Temporal Echoes (Recently Modified Files):"
    echo "------------------------------------------"
    while IFS= read -r file; do
        echo "  File: $file"
        if [ ${#KEYWORDS[@]} -gt 0 ]; then
            KEYWORD_FOUND=0
            for keyword in "${KEYWORDS[@]}"; do
                # -q for quiet, -i for case-insensitive, 2>/dev/null for suppressing errors
                if grep -iq "$keyword" "$file" 2>/dev/null; then
                    if [ "$KEYWORD_FOUND" -eq 0 ]; then
                        echo "    Whispers of urgency:"
                        KEYWORD_FOUND=1
                    fi
                    # Extract lines containing the keyword, prefix with "      - "
                    grep -i -n "$keyword" "$file" 2>/dev/null | sed 's/^/      - /'
                fi
            done
            if [ "$KEYWORD_FOUND" -eq 0 ]; then
                echo "    No specific whispers detected within this echo."
            fi
        fi
        echo ""
    done <<< "$RECENT_FILES"
fi

echo "----------------------------------------------"
echo "Chrono-Compass report complete. Stay vigilant!"
