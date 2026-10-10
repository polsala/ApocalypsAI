#!/bin/bash

# Default values
TARGET_DIR="."
AGE_DAYS=30
DUSTBIN_DIR="" # Default to no dustbin, implies delete if --sweep is used
MODE="report"  # "report" or "sweep"
ACTION="move"  # "move" to dustbin or "delete"

# Whimsical temporary file patterns
TEMP_PATTERNS=(
    "*.tmp" "*.temp" "*~" "#*#" ".DS_Store" "Thumbs.db"
    "*.bak" "*.old" "*.log" "*.swp" "*.swo" "*.swn"
)

# --- Helper Functions ---

display_help() {
    echo "🌌 Nightly Digital Dust Bunny Sweeper 🌌"
    echo "A whimsical utility to find and sweep away the digital dust bunnies (old, temporary, or unused files) from your filesystem."
    echo ""
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --dir <path>      Specify the directory to sweep. Default: current directory ('.')."
    echo "  --age <days>      Files older than this many days are considered dust bunnies. Default: 30 days."
    echo "  --report          (Default) Only report findings, do not perform any actions."
    echo "  --sweep           Perform the sweep action. Requires --delete or --dustbin."
    echo "  --delete          When --sweep is active, permanently delete identified files."
    echo "  --dustbin <path>  When --sweep is active, move identified files to this 'digital dustbin' directory."
    echo "                    If --dustbin is not specified with --sweep, --delete is implied."
    echo "  --help            Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") --dir /var/log --age 7 --report"
    echo "  $(basename "$0") --dir ~/Downloads --sweep --dustbin ~/DigitalDustbin"
    echo "  $(basename "$0") --dir /tmp --age 1 --sweep --delete"
    echo ""
    echo "Remember: Always be cautious when deleting files! Use --report first."
}

# --- Main Logic ---

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dir)
            TARGET_DIR="$2"
            shift
            ;;
        --age)
            AGE_DAYS="$2"
            if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]]; then
                echo "🚨 Error: --age must be a positive integer." >&2
                exit 1
            fi
            shift
            ;;
        --report)
            MODE="report"
            ;;
        --sweep)
            MODE="sweep"
            ;;
        --delete)
            ACTION="delete"
            ;;
        --dustbin)
            ACTION="move"
            DUSTBIN_DIR="$2"
            shift
            ;;
        --help)
            display_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            display_help
            exit 1
            ;;
    esac
    shift
done

# Validate inputs
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "🚨 Error: Target directory '$TARGET_DIR' does not exist or is not a directory." >&2
    exit 1
fi

if [[ "$MODE" == "sweep" ]]; then
    if [[ "$ACTION" == "move" && -z "$DUSTBIN_DIR" ]]; then
        echo "⚠️ Warning: --sweep was used without --dustbin or --delete. Defaulting to --delete."
        ACTION="delete"
    elif [[ "$ACTION" == "move" && ! -d "$DUSTBIN_DIR" ]]; then
        echo "Creating digital dustbin: '$DUSTBIN_DIR'"
        mkdir -p "$DUSTBIN_DIR" || { echo "🚨 Error: Could not create dustbin directory '$DUSTBIN_DIR'." >&2; exit 1; }
    fi
fi

echo "🧹 Initiating Digital Dust Bunny Sweep in '$TARGET_DIR'..."
echo "Looking for files older than $AGE_DAYS days and common temporary patterns."
echo ""

# Find old files
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" -print 2>/dev/null)
if [[ -n "$OLD_FILES" ]]; then
    echo "⏳ Ancient Artifacts (Files older than $AGE_DAYS days):"
    echo "$OLD_FILES"
else
    echo "✨ No ancient artifacts found (files older than $AGE_DAYS days)."
fi
echo ""

# Find temporary pattern files
TEMP_FILES=""
for pattern in "${TEMP_PATTERNS[@]}"; do
    # Use -path to avoid issues with filenames containing newlines, though find -print0 is safer for general use.
    # For simplicity and common patterns, this is usually fine.
    # We'll use -print for easier parsing in bash, assuming no weird filenames for this whimsical tool.
    FOUND_PATTERN_FILES=$(find "$TARGET_DIR" -type f -name "$pattern" -print 2>/dev/null)
    if [[ -n "$FOUND_PATTERN_FILES" ]]; then
        TEMP_FILES+="$FOUND_PATTERN_FILES\n"
    fi
done

if [[ -n "$TEMP_FILES" ]]; then
    echo "🗑️ Ephemeral Remnants (Temporary pattern files):"
    echo -e "$TEMP_FILES" | sort -u
else
    echo "✨ No ephemeral remnants found (temporary pattern files)."
fi
echo ""

# Combine and deduplicate the list of files to be acted upon
ALL_DUST_BUNNIES=$(echo -e "$OLD_FILES\n$TEMP_FILES" | grep -v '^\s*$' | sort -u)

if [[ -z "$ALL_DUST_BUNNIES" ]]; then
    echo "🎉 Your digital space is sparkling clean! No dust bunnies detected."
    exit 0
fi

echo "Total Digital Dust Bunnies identified: $(echo -e "$ALL_DUST_BUNNIES" | wc -l) files."
echo ""

if [[ "$MODE" == "report" ]]; then
    echo "🔍 Report Mode: These files would be acted upon if --sweep was enabled."
    echo "--------------------------------------------------------------------"
    echo -e "$ALL_DUST_BUNNIES"
    echo "--------------------------------------------------------------------"
    echo "To sweep them away, run with --sweep and either --delete or --dustbin <path>."
elif [[ "$MODE" == "sweep" ]]; then
    echo "🧹 Sweep Mode Activated!"
    if [[ "$ACTION" == "delete" ]]; then
        echo "Permanently deleting identified digital dust bunnies..."
        echo -e "$ALL_DUST_BUNNIES" | while IFS= read -r file; do
            echo "  Deleting: $file"
            rm -f "$file"
        done
        echo "✅ Digital dust bunnies have been vanquished!"
    elif [[ "$ACTION" == "move" ]]; then
        echo "Moving identified digital dust bunnies to the digital dustbin: '$DUSTBIN_DIR'..."
        echo -e "$ALL_DUST_BUNNIES" | while IFS= read -r file; do
            echo "  Moving: $file to $DUSTBIN_DIR"
            mv "$file" "$DUSTBIN_DIR/"
        done
        echo "✅ Digital dust bunnies have been safely quarantined in the dustbin!"
    fi
fi

echo ""
echo "🌌 Sweep complete. May your digital realm remain pristine!"
