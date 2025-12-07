#!/bin/bash

# Digital Dust Bunny Sweeper
# Scans for orphaned files, empty directories, and stale cache artifacts

set -e

# Default configuration
SCAN_PATHS=(${1:-"/scan"})
REPORT_FORMAT=${REPORT_FORMAT:-"text"}
MIN_AGE_DAYS=${MIN_AGE_DAYS:-30}
CONFIG_FILE=${2:-""}

# Load configuration if provided
if [[ -f "$CONFIG_FILE" ]]; then
    echo "Loading configuration from $CONFIG_FILE"
    # Extract values from JSON config (simplified for demo)
    SCAN_PATHS=($(grep -o '"scan_paths": \[[^]]*\]' "$CONFIG_FILE" | grep -o '"[^"]*"' | tr -d '"'))
    MIN_AGE_DAYS=$(grep -o '"min_age_days": [0-9]*' "$CONFIG_FILE" | grep -o '[0-9]*')
    REPORT_FORMAT=$(grep -o '"report_format": "[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
fi

# Initialize report
if [[ "$REPORT_FORMAT" == "json" ]]; then
    REPORT_FILE="/scan/dust_bunny_report.json"
    echo '{"scan_results": [' > "$REPORT_FILE"
else
    REPORT_FILE="/scan/dust_bunny_report.txt"
    echo "Digital Dust Bunny Sweeper Report" > "$REPORT_FILE"
    echo "=================================" >> "$REPORT_FILE"
    echo "Scan Date: $(date)" >> "$REPORT_FILE"
    echo "" >> "$REPORT_FILE"
fi

# Function to add JSON entry
add_json_entry() {
    local type="$1"
    local path="$2"
    local details="$3"
    
    if [[ $(tail -c 2 "$REPORT_FILE" | head -c 1) == '[' ]]; then
        echo -n "{"type":"$type","path":"$path","details":"$details"}" >> "$REPORT_FILE"
    else
        echo -n ",{"type":"$type","path":"$path","details":"$details"}" >> "$REPORT_FILE"
    fi
}

# Function to scan for dust bunnies
scan_for_dust_bunnies() {
    local scan_path="$1"
    
    if [[ ! -d "$scan_path" ]]; then
        echo "Warning: Scan path $scan_path does not exist"
        return
    fi
    
    echo "Scanning $scan_path for digital dust bunnies..."
    
    # Find empty directories
    echo "  Checking for empty directories..."
    while IFS= read -r -d '' dir; do
        if [[ "$REPORT_FORMAT" == "json" ]]; then
            add_json_entry "empty_directory" "$dir" "Directory contains no files or subdirectories"
        else
            echo "- Empty Directory: $dir" >> "$REPORT_FILE"
        fi
    done < <(find "$scan_path" -type d -empty -print0 2>/dev/null)
    
    # Find stale cache files
    echo "  Checking for stale cache files..."
    while IFS= read -r -d '' file; do
        if [[ "$REPORT_FORMAT" == "json" ]]; then
            add_json_entry "stale_cache" "$file" "File older than $MIN_AGE_DAYS days"
        else
            echo "- Stale Cache: $file (age: $(stat -c %Y "$file" 2>/dev/null || echo 'unknown') seconds)" >> "$REPORT_FILE"
        fi
    done < <(find "$scan_path" -type f -name "*.cache" -o -name "*.tmp" -o -name "*.log" -mtime +$MIN_AGE_DAYS -print0 2>/dev/null)
    
    # Find orphaned files (files not accessed in a long time)
    echo "  Checking for orphaned files..."
    while IFS= read -r -d '' file; do
        if [[ "$REPORT_FORMAT" == "json" ]]; then
            add_json_entry "orphaned_file" "$file" "File not accessed in $MIN_AGE_DAYS days"
        else
            echo "- Orphaned File: $file (last access: $(stat -c %X "$file" 2>/dev/null || echo 'unknown'))" >> "$REPORT_FILE"
        fi
    done < <(find "$scan_path" -type f -atime +$MIN_AGE_DAYS -print0 2>/dev/null)
}

# Main execution
main() {
    echo "Starting Digital Dust Bunny Sweeper"
    echo "Scan paths: ${SCAN_PATHS[*]}"
    echo "Report format: $REPORT_FORMAT"
    echo "Minimum age: $MIN_AGE_DAYS days"
    echo ""
    
    for path in "${SCAN_PATHS[@]}"; do
        scan_for_dust_bunnies "$path"
    done
    
    if [[ "$REPORT_FORMAT" == "json" ]]; then
        echo ']}' >> "$REPORT_FILE"
    else
        echo "" >> "$REPORT_FILE"
        echo "Scan completed at $(date)" >> "$REPORT_FILE"
        echo "Recommendations: Review the above findings and clean up as appropriate." >> "$REPORT_FILE"
    fi
    
    echo ""
    echo "Report generated at: $REPORT_FILE"
    echo ""
    if [[ "$REPORT_FORMAT" != "json" ]]; then
        echo "Summary of findings:"
        cat "$REPORT_FILE"
    fi
}

# Run the main function
main
