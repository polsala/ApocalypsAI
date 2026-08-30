#!/bin/bash

# --- Configuration ---
DEFAULT_AGE_DAYS=30
TEMP_FILE_PATTERNS=("*.tmp" "*.bak" "*~" ".DS_Store" "Thumbs.db")
EXCLUDE_DIRS=("/proc" "/sys" "/dev" "/run" "/boot" "/mnt" "/media" "/var/lib" "/var/cache") # Common system directories to exclude
# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Helper Functions ---
print_header() {
    echo -e "${BLUE}✨ Nightly Digital Debris Duster ✨${NC}"
    echo -e "${BLUE}------------------------------------${NC}"
}

print_footer() {
    echo -e "${BLUE}------------------------------------${NC}"
    echo -e "${BLUE}🧹 Digital dusting complete! Your system feels lighter. 🌬️${NC}"
}

usage() {
    echo "Usage: $0 [OPTIONS] [TARGET_DIRECTORY...]"
    echo ""
    echo "A whimsical Bash script to identify and suggest cleanup for old, unused, or temporary files and empty directories."
    echo ""
    echo "Options:"
    echo "  -a <days>   Specify age in days for 'old' files (default: ${DEFAULT_AGE_DAYS})."
    echo "  -d          Perform a dry run (no files will be deleted)."
    echo "  -i          Interactive mode: ask for confirmation before each deletion."
    echo "  -h          Display this help message."
    echo ""
    echo "Examples:"
    echo "  $0 /home/user/documents"
    echo "  $0 -a 60 /var/log /tmp"
    echo "  $0 -d -a 7 /home/user"
    echo "  $0 -i /path/to/clean"
    exit 1
}

# --- Main Logic ---
AGE_DAYS=${DEFAULT_AGE_DAYS}
DRY_RUN=false
INTERACTIVE=false
TARGET_DIRS=()

while getopts "a:dih" opt; do
    case ${opt} in
        a ) AGE_DAYS=$OPTARG ;;
        d ) DRY_RUN=true ;;
        i ) INTERACTIVE=true ;;
        h ) usage ;;
        \? ) usage ;;
    esac
done
shift $((OPTIND -1))

if [ "$#" -gt 0 ]; then
    TARGET_DIRS=("$@")
else
    TARGET_DIRS=(".") # Default to current directory if no target specified
fi

# Filter out non-existent or inaccessible directories
VALID_TARGET_DIRS=()
for dir in "${TARGET_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        VALID_TARGET_DIRS+=("$dir")
    else
        echo -e "${YELLOW}Warning: Directory '$dir' not found or not accessible. Skipping.${NC}"
    fi
done

if [ ${#VALID_TARGET_DIRS[@]} -eq 0 ]; then
    echo -e "${RED}Error: No valid target directories specified or found. Exiting.${NC}"
    exit 1
fi

print_header

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}💨 Dry Run Mode: No actual deletions will occur. 💨${NC}"
fi
echo -e "${BLUE}Scanning for digital debris in: ${VALID_TARGET_DIRS[*]}${NC}"
echo -e "${BLUE}Looking for files older than ${AGE_DAYS} days and common temporary files.${NC}"
echo ""

DEBRIS_FOUND=false

# Build exclusion string for find
EXCLUDE_FIND_ARGS=""
for dir in "${EXCLUDE_DIRS[@]}"; do
    EXCLUDE_FIND_ARGS+=" -not -path \"${dir}/*\""
done
# Add a space at the beginning if not empty, to separate from previous arguments
if [ -n "$EXCLUDE_FIND_ARGS" ]; then
    EXCLUDE_FIND_ARGS=" ${EXCLUDE_FIND_ARGS}"
fi

# --- Find Old Files ---
echo -e "${YELLOW}🔍 Searching for ancient scrolls (files older than ${AGE_DAYS} days)...${NC}"
OLD_FILES=$(eval "find \"${VALID_TARGET_DIRS[@]}\" -type f -mtime +${AGE_DAYS}${EXCLUDE_FIND_ARGS} -print 2>/dev/null")
if [ -n "$OLD_FILES" ]; then
    DEBRIS_FOUND=true
    echo -e "${GREEN}Found these dusty relics:${NC}"
    echo "$OLD_FILES" | while IFS= read -r file; do
        echo -e "  - ${file}"
        if [ "$DRY_RUN" = false ]; then
            if [ "$INTERACTIVE" = true ]; then
                read -p "  🧹 Sweep away '${file}'? (y/N) " -n 1 -r
                echo ""
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rm -f "$file" && echo -e "    ${GREEN}Swept!${NC}" || echo -e "    ${RED}Failed to sweep.${NC}"
                else
                    echo -e "    ${YELLOW}Skipped.${NC}"
                fi
            else
                rm -f "$file" && echo -e "    ${GREEN}Swept!${NC}" || echo -e "    ${RED}Failed to sweep.${NC}"
            fi
        fi
    done
else
    echo -e "${GREEN}No ancient scrolls found. Your archives are spry!${NC}"
fi
echo ""

# --- Find Temporary Files ---
echo -e "${YELLOW}🔍 Searching for fleeting wisps (common temporary files)...${NC}"
TEMP_FILES_LIST=""
for pattern in "${TEMP_FILE_PATTERNS[@]}"; do
    TEMP_FILES_LIST+=$(eval "find \"${VALID_TARGET_DIRS[@]}\" -type f -name \"$pattern\"${EXCLUDE_FIND_ARGS} -print 2>/dev/null")
    TEMP_FILES_LIST+="\n" # Add newline for separation
done
TEMP_FILES_LIST=$(echo -e "$TEMP_FILES_LIST" | sort -u) # Remove duplicates and sort

if [ -n "$TEMP_FILES_LIST" ]; then
    DEBRIS_FOUND=true
    echo -e "${GREEN}Found these transient specks:${NC}"
    echo -e "$TEMP_FILES_LIST" | while IFS= read -r file; do
        if [ -n "$file" ]; then # Ensure file is not empty
            echo -e "  - ${file}"
            if [ "$DRY_RUN" = false ]; then
                if [ "$INTERACTIVE" = true ]; then
                    read -p "  🧹 Sweep away '${file}'? (y/N) " -n 1 -r
                    echo ""
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        rm -f "$file" && echo -e "    ${GREEN}Swept!${NC}" || echo -e "    ${RED}Failed to sweep.${NC}"
                    else
                        echo -e "    ${YELLOW}Skipped.${NC}"
                    fi
                else
                    rm -f "$file" && echo -e "    ${GREEN}Swept!${NC}" || echo -e "    ${RED}Failed to sweep.${NC}"
                fi
            fi
        fi
    done
else
    echo -e "${GREEN}No fleeting wisps found. Your temporary zones are pristine!${NC}"
fi
echo ""

# --- Find Empty Directories ---
echo -e "${YELLOW}🔍 Searching for hollow caverns (empty directories)...${NC}"
EMPTY_DIRS=$(eval "find \"${VALID_TARGET_DIRS[@]}\" -type d -empty${EXCLUDE_FIND_ARGS} -print 2>/dev/null")
if [ -n "$EMPTY_DIRS" ]; then
    DEBRIS_FOUND=true
    echo -e "${GREEN}Found these vacant spaces:${NC}"
    echo "$EMPTY_DIRS" | while IFS= read -r dir; do
        echo -e "  - ${dir}"
        if [ "$DRY_RUN" = false ]; then
            if [ "$INTERACTIVE" = true ]; then
                read -p "  🧹 Collapse '${dir}'? (y/N) " -n 1 -r
                echo ""
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    rmdir "$dir" && echo -e "    ${GREEN}Collapsed!${NC}" || echo -e "    ${RED}Failed to collapse.${NC}"
                else
                    echo -e "    ${YELLOW}Skipped.${NC}"
                fi
            else
                rmdir "$dir" && echo -e "    ${GREEN}Collapsed!${NC}" || echo -e "    ${RED}Failed to collapse.${NC}"
            fi
        fi
    done
else
    echo -e "${GREEN}No hollow caverns found. Every space is purposeful!${NC}"
fi
echo ""

if [ "$DEBRIS_FOUND" = false ]; then
    echo -e "${GREEN}✨ Your digital realm is sparkling clean! No debris detected. ✨${NC}"
fi

print_footer
