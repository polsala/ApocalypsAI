#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <file_or_dir_path> [--dry-run]"
    echo "Scans log files for sensitive data patterns and redacts them."
    echo "  <file_or_dir_path> : Path to a log file or a directory containing log files."
    echo "  --dry-run          : Simulate redaction without modifying files."
    exit 1
}

# Check for required arguments
if [ -z "$1" ]; then
    usage
fi

TARGET_PATH="$1"
DRY_RUN=false

if [ "$2" == "--dry-run" ]; then
    DRY_RUN=true
fi

# Define redaction patterns and replacement string
REDACTED_STRING="[REDACTED]"

# Regex patterns for sensitive data
# Rationale: These regexes are simplified for demonstration.
# In a real-world scenario, they would be much more robust and configurable.
# For example, API keys often have specific prefixes or lengths.
# IP addresses are common, emails are common, and "password=" is a simple indicator.
# We use extended regex (-E) for sed.
declare -a PATTERNS=(
    "([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})" # Email addresses
    "((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))" # IPv4 addresses
    "(API_KEY=[A-Za-z0-9]{20,40})" # Generic API key pattern (e.g., API_KEY=...)
    "(password=[^\\s&\"']{6,})" # Simple password= value (avoids matching 'password' itself)
)

# Function to process a single file
process_file() {
    local file="$1"
    local temp_file="${file}.tmp.$$"
    local modified=false

    echo "Processing: $file"

    if [ "$DRY_RUN" = true ]; then
        echo "  (Dry run) Would redact sensitive data in $file"
        # Simulate redaction by piping to /dev/null or stdout
        for pattern in "${PATTERNS[@]}"; do
            if grep -qE "$pattern" "$file"; then
                echo "    Found pattern: $pattern"
                modified=true
            fi
        done
        if [ "$modified" = true ]; then
            echo "  (Dry run) Sensitive data detected. Output would be:"
            # Use sed to show what *would* be redacted
            local sed_command=""
            for pattern in "${PATTERNS[@]}"; do
                sed_command+="s/$pattern/$REDACTED_STRING/g;"
            done
            sed -E "$sed_command" "$file"
        else
            echo "  (Dry run) No sensitive data found."
        fi
    else
        # Actual redaction
        cp "$file" "$temp_file" # Create a temporary copy to work on

        local sed_command=""
        for pattern in "${PATTERNS[@]}"; do
            # Check if pattern exists before applying sed to avoid unnecessary file writes
            if grep -qE "$pattern" "$file"; then
                sed_command+="s/$pattern/$REDACTED_STRING/g;"
                modified=true
            fi
        fi

        if [ "$modified" = true ]; then
            echo "  Redacting sensitive data in $file..."
            # Apply all redactions in one sed command for efficiency
            sed -E "$sed_command" "$file" > "$temp_file"
            mv "$temp_file" "$file"
            echo "  Redaction complete for $file."
        else
            echo "  No sensitive data found in $file. No changes made."
            rm "$temp_file" # Clean up temp file if no changes
        fi
    fi
}

# Main logic
if [ -f "$TARGET_PATH" ]; then
    process_file "$TARGET_PATH"
elif [ -d "$TARGET_PATH" ]; then
    echo "Scanning directory: $TARGET_PATH"
    find "$TARGET_PATH" -type f -print0 | while IFS= read -r -d $'\0' file; do
        # Only process files that look like logs (e.g., .log, .txt, or no extension)
        # Rationale: Avoids processing binaries or other non-log files.
        # This is a heuristic and can be improved.
        if [[ "$file" =~ \.(log|txt|json|yml|yaml)$ || ! "$file" =~ \. ]]; then
            process_file "$file"
        else
            echo "Skipping non-log file: $file"
        fi
    done
else
    echo "Error: '$TARGET_PATH' is not a valid file or directory."
    usage
fi

echo "Scrubbing complete."
