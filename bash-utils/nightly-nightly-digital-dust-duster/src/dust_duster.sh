#!/bin/bash

# Nightly Digital Dust Duster
# A bash utility to identify and report on old, forgotten files in specified directories.

# Function to display usage information
usage() {
    echo "Usage: $0 <directory> <age_in_days> [min_size_in_kb]" >&2
    echo "" >&2
    echo "  <directory>      : The path to the directory you want to scour." >&2
    echo "  <age_in_days>    : Files older than this many days will be reported." >&2
    echo "  [min_size_in_kb] : (Optional) Only report files larger than this size in kilobytes." >&2
    echo "" >&2
    echo "Example: $0 /var/log 90" >&2
    echo "Example: $0 ~/ 365 10240" >&2
    exit 1
}

# Check if correct number of arguments are provided
if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    usage
fi

TARGET_DIR="$1"
AGE_DAYS="$2"
MIN_SIZE_KB="$3"

# Validate directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' not found." >&2
    exit 1
fi

# Validate age_in_days is a positive integer
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -le 0 ]; then
    echo "Error: Age in days must be a positive integer." >&2
    exit 1
fi

# Construct the size argument for find
SIZE_ARG=""
if [ -n "$MIN_SIZE_KB" ]; then
    # Validate min_size_in_kb is a positive integer
    if ! [[ "$MIN_SIZE_KB" =~ ^[0-9]+$ ]] || [ "$MIN_SIZE_KB" -le 0 ]; then
        echo "Error: Minimum size in KB must be a positive integer." >&2
        exit 1
    fi
    # find's -size uses 'k' for KB
    SIZE_ARG="-size +${MIN_SIZE_KB}k"
fi

echo "--- Nightly Digital Dust Duster Report ---"
echo "Scouring: $TARGET_DIR"
echo "Files older than: $AGE_DAYS days"
[ -n "$MIN_SIZE_KB" ] && echo "Minimum size: $MIN_SIZE_KB KB"
echo "----------------------------------------"

# Mock rationale: The `find` command is a standard system utility. Its behavior is deterministic
# when operating on a controlled, temporary filesystem created by the test script.
# No external network calls or non-deterministic elements are involved.

# Find files and print their size (bytes), modification date, and path using tab as separator.
# Then pipe to a while loop to format the output.
# %s: size in bytes
# %TY-%Tm-%Td %TH:%TM:%TS: last modification date and time
# %p: filename

find "$TARGET_DIR" -type f -mtime "+$AGE_DAYS" ${SIZE_ARG} -printf "%s\t%TY-%Tm-%Td %TH:%TM:%TS\t%p\n" | \
while IFS=$'\t' read -r size_bytes mod_date_time file_path; do
    # Calculate size in KB, rounding up
    FILE_SIZE_KB=$(( (size_bytes + 1023) / 1024 ))
    echo "  - Size: ${FILE_SIZE_KB}KB, Modified: $mod_date_time, Path: $file_path"
done

echo "----------------------------------------"
echo "Digital dust duster complete. Happy scavenging!"
