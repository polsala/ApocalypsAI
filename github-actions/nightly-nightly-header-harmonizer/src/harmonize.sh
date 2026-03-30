#!/bin/bash
set -euo pipefail

HEADER_CONTENT="$1"
FILE_PATTERNS="$2"
FIX_MODE="$3" # "true" or "false"

IFS=',' read -ra PATTERNS <<< "$FILE_PATTERNS"

# Function to get comment prefix/suffix based on file extension
get_comment_style() {
    local filename="$1"
    local extension="${filename##*.}"
    case "$extension" in
        py|sh|yml|yaml|md|txt) echo "#" "" ;;
        js|ts|jsx|tsx|go|java|c|cpp|h|hpp) echo "//" "" ;;
        html|xml) echo "<!--" "-->" ;;
        css) echo "/*" "*/" ;;
        *) echo "" "" ;;
    esac
}

# Function to format header content with comment style
format_header() {
    local content="$1"
    local prefix="$2"
    local suffix="$3"
    local formatted_header=""
    IFS=$'\n' read -ra lines <<< "$content"
    for line in "${lines[@]}"; do
        if [[ -n "$suffix" ]]; then # Block comments
            formatted_header+="$prefix $line $suffix\n"
        else # Line comments
            formatted_header+="$prefix $line\n"
        fi
    done
    echo -e "$formatted_header"
}

NON_COMPLIANT_FILES=""
ALL_FILES_CHECKED=0

for pattern in "${PATTERNS[@]}"; do
    # Use find with -print0 and xargs -0 to handle filenames with spaces or special characters
    while IFS= read -r -d $'' file; do
        ALL_FILES_CHECKED=1
        
        read -r prefix suffix <<< $(get_comment_style "$file")
        
        if [[ -z "$prefix" && -z "$suffix" ]]; then
            echo "Skipping file $file: No known comment style for extension." >&2
            continue
        fi

        FORMATTED_HEADER=$(format_header "$HEADER_CONTENT" "$prefix" "$suffix")
        HEADER_LINE_COUNT=$(echo -e "$FORMATTED_HEADER" | wc -l)

        # Check if file starts with the formatted header
        # Mock rationale: `head` and `diff` are standard shell utilities,
        # their behavior is deterministic for file content. `head` reads the beginning
        # of a file, and `diff -q` compares two inputs silently, returning 0 if identical.
        if ! head -n "$HEADER_LINE_COUNT" "$file" | diff -q - <(echo -e "$FORMATTED_HEADER"); then
            echo "File $file is missing or has an incorrect header." >&2
            NON_COMPLIANT_FILES+="$file\n"
            if [[ "$FIX_MODE" == "true" ]]; then
                echo "Fixing header for $file..." >&2
                # Prepend the header
                # Mock rationale: `cat` and `mv` are standard shell utilities,
                # their behavior is deterministic for file content. `cat` concatenates
                # the header with the original file, and `mv` replaces the original.
                echo -e "$FORMATTED_HEADER" | cat - "$file" > "$file.tmp" && mv "$file.tmp" "$file"
                echo "Header added to $file." >&2
            fi
        else
            echo "File $file has the correct header." >&2
        fi
    done < <(find . -type f -name "$pattern" -print0)
done

if [[ "$ALL_FILES_CHECKED" -eq 0 ]]; then
    echo "No files matched the provided patterns: $FILE_PATTERNS" >&2
    exit 1 # Indicate failure if no files were processed
fi

# Set output for non_compliant_files
# This syntax is specific to GitHub Actions composite runs for multi-line outputs
if [[ -n "$NON_COMPLIANT_FILES" ]]; then
    echo "::error file=harmonize.sh::The following files are non-compliant:\n$NON_COMPLIANT_FILES" >&2
    echo "non_compliant_files<<EOF" >> "$GITHUB_OUTPUT"
    echo -e "$NON_COMPLIANT_FILES" >> "$GITHUB_OUTPUT"
    echo "EOF" >> "$GITHUB_OUTPUT"
    exit 1 # Indicate failure
else
    echo "All matched files are compliant." >&2
    echo "non_compliant_files=" >> "$GITHUB_OUTPUT"
fi
