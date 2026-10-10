#!/bin/bash

# Default values
DEFAULT_DIR="$HOME/Downloads"
DEFAULT_AGE_DAYS=30
SWEEP_MODE=0 # 0 for dry-run, 1 for interactive sweep, 2 for force sweep

# Whimsical messages
MESSAGES=(
    "The digital dust bunnies are gathering! Let's find them..."
    "Scanning for forgotten digital detritus..."
    "A faint whisper of old files... time to investigate!"
    "Unearthing the relics of your digital past..."
    "Dusting off the corners of your filesystem..."
)
RANDOM_MESSAGE=${MESSAGES[$RANDOM % ${#MESSAGES[@]}]}

# Function to display usage
usage() {
    echo "Usage: $(basename "$0") [OPTIONS] [DIRECTORY]"
    echo "A whimsical Bash script to identify and optionally sweep away digital dust bunnies (old, unused files)."
    echo ""
    echo "Options:"
    echo "  -d <days>   Specify the age in days (default: $DEFAULT_AGE_DAYS)."
    echo "  -s          Enable interactive sweep mode. You'll be prompted before sweeping."
    echo "  -f          Enable force sweep mode. Files will be moved to a dustbin without prompt."
    echo "  -h          Display this help message."
    echo ""
    echo "Arguments:"
    echo "  DIRECTORY   The directory to scan (default: $DEFAULT_DIR)."
    echo ""
    echo "Example: $(basename "$0") -d 60 -s ~/Documents"
    exit 1
}

# Parse arguments
while getopts "d:sfh" opt; do
    case "$opt" in
        d) AGE_DAYS="$OPTARG" ;;
        s) SWEEP_MODE=1 ;;
        f) SWEEP_MODE=2 ;;
        h) usage ;;
        *) usage ;;
    esac
done
shift $((OPTIND-1))

TARGET_DIR="${1:-$DEFAULT_DIR}"
AGE_DAYS="${AGE_DAYS:-$DEFAULT_AGE_DAYS}"

# Validate directory
if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Error: Directory '$TARGET_DIR' not found or is not a directory."
    exit 1
fi

echo "🧹 $RANDOM_MESSAGE"
echo "Searching for files older than $AGE_DAYS days in '$TARGET_DIR'..."
echo ""

# Find old files
# Mock rationale: In tests, 'find' will be mocked to return predefined file paths.
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$AGE_DAYS" 2>/dev/null)

if [[ -z "$OLD_FILES" ]]; then
    echo "✨ No digital dust bunnies found! Your filesystem is sparkling clean."
    exit 0
fi

echo "Found these dusty relics:"
echo "$OLD_FILES" | sed 's/^/  - /' # Prepend bullet points

if [[ "$SWEEP_MODE" -eq 0 ]]; then
    echo ""
    echo "This was a dry run. To sweep them away, run with '-s' for interactive or '-f' for force sweep."
    exit 0
fi

# Prepare digital dustbin
DUSTBIN_DIR="$HOME/.digital_dustbin_$(date +%Y%m%d%H%M%S)"
# Mock rationale: 'mkdir' will be mocked to prevent actual directory creation in tests.
mkdir -p "$DUSTBIN_DIR" || { echo "Error: Could not create digital dustbin at '$DUSTBIN_DIR'."; exit 1; }
echo ""
echo "Preparing the Digital Dustbin at '$DUSTBIN_DIR'..."

if [[ "$SWEEP_MODE" -eq 1 ]]; then
    read -p "Do you want to sweep these digital dust bunnies into the dustbin? (y/N): " -n 1 -r
    echo ""
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Phew! Digital dust bunnies spared. They'll live to see another day."
        # Mock rationale: 'rmdir' will be mocked to prevent actual directory removal in tests.
        rmdir "$DUSTBIN_DIR" 2>/dev/null # Clean up empty dustbin if not used
        exit 0
    fi
fi

echo "Sweeping away the digital dust bunnies..."
echo "$OLD_FILES" | while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        # Mock rationale: 'mv' will be mocked to log its calls instead of moving files.
        mv "$file" "$DUSTBIN_DIR/"
        echo "  Moved: $file"
    else
        echo "  Skipped (not a file or already moved): $file"
    fi
done

echo ""
echo "🧹 All digital dust bunnies have been swept into the dustbin! Your system feels lighter."
echo "You can review them in '$DUSTBIN_DIR' and delete them permanently when ready."
