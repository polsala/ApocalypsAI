#!/bin/bash

# Nightly Digital Dust Bunny Hunt - A whimsical system cleanup utility

DEFAULT_SCAN_DIR="/tmp"
DEFAULT_AGE_DAYS=7

SCAN_DIR="${1:-$DEFAULT_SCAN_DIR}"
AGE_DAYS="${2:-$DEFAULT_AGE_DAYS}"
DRY_RUN=false

# Check for --dry-run argument
if [[ "$3" == "--dry-run" ]]; then
    DRY_RUN=true
fi

echo "🌌 Initiating Nightly Digital Dust Bunny Hunt..."
echo "Scanning for digital dust bunnies (files older than $AGE_DAYS days) in: $SCAN_DIR"
echo "---------------------------------------------------------------------"

# Find old files
# Mock rationale: In tests, 'find' will be mocked to output specific file paths
# within a controlled temporary directory, allowing deterministic results.
DUST_BUNNIES=$(find "$SCAN_DIR" -type f -mtime +"$AGE_DAYS" -print 2>/dev/null)

if [ -z "$DUST_BUNNIES" ]; then
    echo "✨ All clear! No digital dust bunnies detected in $SCAN_DIR. Your system is sparkling!"
else
    echo "🧹 Behold! The following digital dust bunnies have been unearthed:"
    echo "$DUST_BUNNIES" | while IFS= read -r file; do
        echo "  - $file"
    done
    echo ""

    if $DRY_RUN; then
        echo "🔍 This was a dry run. No dust bunnies were swept away."
    else
        read -p "Would you like to sweep these digital dust bunnies away? (y/N): " -n 1 -r
        echo "" # Newline after prompt
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "🌪️ Sweeping away the digital detritus..."
            # Mock rationale: 'rm' will be mocked in tests to verify its invocation
            # without actually deleting files from the test environment.
            echo "$DUST_BUNNIES" | xargs rm -f 2>/dev/null
            echo "✅ Digital dust bunnies swept away! Your system feels lighter."
        else
            echo "😌 Understood. The dust bunnies remain, for now. Perhaps they're sentimental."
        fi
    fi
fi

echo "---------------------------------------------------------------------"
echo "🌌 Nightly Digital Dust Bunny Hunt complete."
