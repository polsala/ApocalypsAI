#!/bin/bash

# Nightly Digital Dust Bunny Sweeper

# Default values
TARGET_DIR="."
AGE_DAYS=30
SIZE_MB=100
PATTERNS=()
FORCE_DELETE=false

# Whimsical colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo -e "${GREEN}Nightly Digital Dust Bunny Sweeper${NC}"
    echo "Usage: $0 [-d <directory>] [-a <days>] [-s <megabytes>] [-p <pattern>] [-f] [-h]"
    echo ""
    echo "Options:"
    echo "  -d <directory>   : Target directory to sweep. Defaults to current (.)."
    echo "  -a <days>        : Identify files older than <days> (modification time). Defaults to ${AGE_DAYS}."
    echo "  -s <megabytes>   : Identify files larger than <megabytes> (in MB). Defaults to ${SIZE_MB}."
    echo "  -p <pattern>     : Identify files matching a specific glob <pattern> (e.g., *.tmp, cache/*)."
    echo "                     Can be used multiple times."
    echo "  -f               : Force deletion without confirmation. Use with extreme caution!"
    echo "  -h               : Display this help message."
    echo ""
    echo "Example: $0 -d /var/log -a 7 -s 50 -p \"*.gz\" -p \"*.log\""
    exit 1
}

# Parse command-line arguments
while getopts "d:a:s:p:fh" opt; do
    case ${opt} in
        d ) TARGET_DIR=$OPTARG ;;
        a ) AGE_DAYS=$OPTARG ;;
        s ) SIZE_MB=$OPTARG ;;
        p ) PATTERNS+=("$OPTARG") ;;
        f ) FORCE_DELETE=true ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done
shift $((OPTIND -1))

# Validate target directory
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Target directory '$TARGET_DIR' does not exist.${NC}"
    exit 1
fi

echo -e "${GREEN}Initiating Digital Dust Bunny Sweep in '$TARGET_DIR'...${NC}"

# Build find criteria
CRITERIA_PARTS=()

if [ -n "$AGE_DAYS" ] && [ "$AGE_DAYS" -gt 0 ]; then
    CRITERIA_PARTS+=("-mtime" "+$AGE_DAYS")
fi

if [ -n "$SIZE_MB" ] && [ "$SIZE_MB" -gt 0 ]; then
    CRITERIA_PARTS+=("-size" "+${SIZE_MB}M")
fi

for pattern in "${PATTERNS[@]}"; do
    CRITERIA_PARTS+=("-name" "$pattern")
done

# If no criteria at all, use default age/size
if [ ${#CRITERIA_PARTS[@]} -eq 0 ]; then
    echo -e "${YELLOW}No specific criteria provided. Using default: older than ${AGE_DAYS} days OR larger than ${SIZE_MB}MB.${NC}"
    CRITERIA_PARTS+=("-mtime" "+$AGE_DAYS" "-o" "-size" "+${SIZE_MB}M")
fi

# Combine all parts with -o
FIND_EXPRESSION=()
FIRST=true
for part in "${CRITERIA_PARTS[@]}"; do
    if [ "$FIRST" = false ]; then
        FIND_EXPRESSION+=("-o")
    fi
    FIND_EXPRESSION+=("$part")
    FIRST=false
done

# Find the files
echo -e "${YELLOW}Searching for digital dust bunnies...${NC}"
# Use -print0 and xargs -0 for safe handling of filenames with spaces/special chars
DUST_BUNNIES=$(find "$TARGET_DIR" -type f \( "${FIND_EXPRESSION[@]}" \) -print0)

if [ -z "$DUST_BUNNIES" ]; then
    echo -e "${GREEN}No digital dust bunnies found. Your digital workspace is sparkling clean! ✨${NC}"
    exit 0
fi

echo -e "${YELLOW}Found these digital dust bunnies:${NC}"
echo "$DUST_BUNNIES" | xargs -0 -I {} echo "  - {}"

if [ "$FORCE_DELETE" = true ]; then
    echo -e "${RED}Force deletion enabled. Sweeping away the clutter...${NC}"
    echo "$DUST_BUNNIES" | xargs -0 rm -v
    echo -e "${GREEN}Digital workspace sparkling clean! ✨${NC}"
else
    echo -e "${YELLOW}Do you wish to sweep these digital dust bunnies away? (y/N)${NC}"
    read -r CONFIRMATION
    if [[ "$CONFIRMATION" =~ ^[Yy]$ ]]; then
        echo -e "${RED}Sweeping away the clutter...${NC}"
        echo "$DUST_BUNNIES" | xargs -0 rm -v
        echo -e "${GREEN}Digital workspace sparkling clean! ✨${NC}"
    else
        echo -e "${YELLOW}Digital dust bunnies spared. They'll be back...${NC}"
    fi
fi
