#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

DEFAULT_DIR="."
DEFAULT_AGE_DAYS=7
DRY_RUN=false
CONFIRM=true

# Whimsical messages
MESSAGES=(
    "The digital dust bunnies are gathering... time for a sweep!"
    "A faint whisper from the void... 'Cleanse your digital realm!'"
    "Your filesystem is feeling a bit... cluttered. Let's tidy up!"
    "Behold, the accumulated digital detritus! Shall we banish it?"
    "Even in the apocalypse, a clean filesystem brings joy. Or at least, less despair."
)

# Function to display a random whimsical message
display_whimsical_message() {
    local num_messages=${#MESSAGES[@]}
    local random_index=$(( RANDOM % num_messages ))
    echo -e "\n🧹 ${MESSAGES[$random_index]}\n"
}

# Function to display usage
usage() {
    echo "Usage: $0 [-d <directory>] [-a <age_in_days>] [-n] [-y]"
    echo "  -d <directory>   : Directory to scan (default: current directory)"
    echo "  -a <age_in_days> : Files older than this many days will be considered dust bunnies (default: 7)"
    echo "  -n               : Dry run (only show what would be swept, don't ask for confirmation or delete)"
    echo "  -y               : Assume 'yes' to all prompts (use with caution!)"
    echo "  -h               : Display this help message"
    exit 1
}

# Parse arguments
while getopts "d:a:nyh" opt; do
    case ${opt} in
        d )
            TARGET_DIR=$OPTARG
            ;;
        a )
            DEFAULT_AGE_DAYS=$OPTARG
            ;;
        n )
            DRY_RUN=true
            CONFIRM=false
            ;;
        y )
            CONFIRM=false
            ;;
        h )
            usage
            ;;
        \? )
            echo "Invalid option: -$OPTARG" >&2
            usage
            ;;
    esac
done
shift $((OPTIND -1))

TARGET_DIR=${TARGET_DIR:-$DEFAULT_DIR}

echo "Scanning '$TARGET_DIR' for digital dust bunnies older than $DEFAULT_AGE_DAYS days..."

display_whimsical_message

# Find old files
OLD_FILES=$(find "$TARGET_DIR" -type f -mtime +"$DEFAULT_AGE_DAYS" 2>/dev/null)
# Find empty directories
EMPTY_DIRS=$(find "$TARGET_DIR" -type d -empty 2>/dev/null | grep -v "^$TARGET_DIR$") # Exclude the target dir itself if it's empty

FOUND_ANY=false

if [ -n "$OLD_FILES" ]; then
    FOUND_ANY=true
    echo -e "\n✨ Found these ancient scrolls (files older than $DEFAULT_AGE_DAYS days):"
    echo "$OLD_FILES" | sed 's/^/  - /'
fi

if [ -n "$EMPTY_DIRS" ]; then
    FOUND_ANY=true
    echo -e "\n🕳️ Discovered these forgotten caverns (empty directories):"
    echo "$EMPTY_DIRS" | sed 's/^/  - /'
fi

if ! $FOUND_ANY; then
    echo -e "\n🎉 Your digital realm is sparkling clean! No dust bunnies found. For now..."
    exit 0
fi

if $DRY_RUN; then
    echo -e "\n(Dry run complete. No changes were made.)"
    exit 0
fi

if $CONFIRM; then
    read -p $'\nReady to unleash the sweeping magic? (y/N) ' -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Phew! Digital dust bunnies get to live another day. No sweeping performed."
        exit 0
    fi
fi

echo -e "\n🌪️ Initiating digital dust bunny sweep..."

SWEEP_COUNT=0

# Sweep old files
if [ -n "$OLD_FILES" ]; then
    echo "$OLD_FILES" | while IFS= read -r file; do
        if rm -v "$file"; then
            echo "  🧹 Swept away: $file"
            ((SWEEP_COUNT++))
        else
            echo "  ⚠️ Failed to sweep: $file"
        fi
    done
fi

# Sweep empty directories
if [ -n "$EMPTY_DIRS" ]; then
    # Sort in reverse order to delete subdirectories before parent directories
    echo "$EMPTY_DIRS" | sort -r | while IFS= read -r dir; do
        if rmdir -v "$dir"; then
            echo "  🧹 Swept away empty cavern: $dir"
            ((SWEEP_COUNT++))
        else
            echo "  ⚠️ Failed to sweep empty cavern: $dir (might not be empty anymore or permissions issue)"
        fi
    done
fi

echo -e "\n✨ Sweep complete! $SWEEP_COUNT digital dust bunnies banished to the void."
