#!/bin/bash

# Nightly Echo Purifier: Detects and reports duplicate files across specified directories.
# Whimsical-yet-useful: Purifies 'temporal echo chambers' of redundant data.

# --- Configuration ---
# Path to store temporary checksum data
TEMP_FILE="$(mktemp)"

# --- Functions ---

# Function to clean up temporary files on exit
cleanup() {
    rm -f "$TEMP_FILE"
}
trap cleanup EXIT

# Function to display usage information
usage() {
    echo "Usage: $(basename "$0") <directory1> [directory2 ...]"
    echo "Detects and reports duplicate files across specified directories using MD5 checksums."
    echo "Example: $(basename "$0") /path/to/data /path/to/backups"
    exit 1
}

# --- Main Logic ---

# Check if at least one directory is provided
if [ "$#" -eq 0 ]; then
    usage
fi

# Process each directory provided as an argument
for dir in "$@"; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' not found or is not a directory." >&2
        exit 1
    fi
    echo "Scanning '$dir' for temporal echoes..." >&2
    # Find all regular files and calculate their MD5 checksums
    # Using 'md5sum' directly on find's output to handle filenames with spaces/special chars correctly
    find "$dir" -type f -print0 | xargs -0 md5sum >> "$TEMP_FILE"
done

# Sort the checksums and identify duplicates
# The 'sort' command sorts by the checksum (first field)
# The 'awk' command then processes the sorted output:
#   - It keeps track of the current checksum and the count of files with that checksum.
#   - When a new checksum is encountered, if the previous checksum had more than one file, it prints the group.
#   - Finally, it handles the last group after the loop finishes.

if [ ! -s "$TEMP_FILE" ]; then
    echo "No files found to process or an error occurred during checksum calculation." >&2
    exit 0
fi

# Sort by checksum, then by filename for stable output
sorted_checksums=$(sort -k1,1 "$TEMP_FILE")

# Use awk to find and format duplicate groups
awk 'BEGIN {current_checksum = ""; count = 0;}
     { 
       checksum = $1;
       # Reconstruct filename, handling spaces in filenames
       filename = substr($0, index($0,$2));

       if (checksum != current_checksum) {
         if (count > 1) {
           print "\nDuplicate Group (Checksum: " current_checksum "):";
           for (i=1; i<=count; i++) {
             print "  - " files[i];
           }
         }
         current_checksum = checksum;
         count = 1;
         files[1] = filename;
       } else {
         count++;
         files[count] = filename;
       }
     }
     END {
       if (count > 1) {
         print "\nDuplicate Group (Checksum: " current_checksum "):";
         for (i=1; i<=count; i++) {
           print "  - " files[i];
         }
       }
     }' <<< "$sorted_checksums"

echo "\nTemporal echo purification complete." >&2
