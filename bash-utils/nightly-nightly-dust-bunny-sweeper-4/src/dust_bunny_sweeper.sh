#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <target_directory> <age_in_days>"
    echo "Example: $0 /tmp 7"
    echo "Sweeps away 'temporal dust bunnies' (files/directories) older than <age_in_days> in <target_directory>."
    exit 1
}

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    usage
fi

TARGET_DIR="$1"
AGE_DAYS="$2"

# Validate target directory
if [ ! -d "$TARGET_DIR" ]; then
    echo "Oh dear! The 'temporal vortex' at '$TARGET_DIR' does not exist or is not a directory. Cannot sweep!"
    exit 1
fi

# Validate age in days
if ! [[ "$AGE_DAYS" =~ ^[0-9]+$ ]] || [ "$AGE_DAYS" -lt 0 ]; then
    echo "The 'temporal age' must be a non-negative number of days. How old are these dust bunnies, really?"
    exit 1
fi

echo "Initiating Temporal Dust Bunny Sweeper Protocol in '$TARGET_DIR' for items older than $AGE_DAYS days..."

# Find and delete files/directories older than AGE_DAYS
# -mtime +N: file's data was last modified N*24 hours ago. +7 means older than 7 days.
# -print0: prints the full file name on the standard output, followed by a null character.
# xargs -0: reads items from standard input, delimited by null characters.
# rm -rf: remove files and directories recursively and forcefully.
# Mock rationale: In a real scenario, `rm -rf` would delete files. For testing, we'll run this in a controlled temp environment.
# The `find` command is robust and its output is predictable.
# The `rm -rf` command is standard. The core logic is finding the correct files.
# The test script will create a temporary directory and files with specific timestamps to verify deletion.
# The output of `find` will be captured and checked in tests to ensure correct identification.
# The actual deletion will be verified by checking the filesystem after the script runs in the test environment.
found_bunnies=$(find "$TARGET_DIR" -maxdepth 1 -mindepth 1 -mtime +"$AGE_DAYS" -print0)

if [ -z "$found_bunnies" ]; then
    echo "Phew! No temporal dust bunnies found older than $AGE_DAYS days in '$TARGET_DIR'. All clear!"
else
    echo "Aha! Detected some ancient temporal dust bunnies. Preparing for a thorough sweep..."
    # Use a loop to process each item found by find, for better error handling and logging
    # This also makes it easier to mock/control in tests if needed, though direct deletion is fine for this test strategy.
    while IFS= read -r -d $'\0' bunny; do
        echo "Sweeping away: '$bunny' (a particularly dusty temporal specimen!)"
        rm -rf "$bunny" # Mock rationale: This will actually delete files in the test environment.
                        # The test setup ensures this is safe and isolated.
    done <<< "$found_bunnies"
    echo "Temporal Dust Bunny Sweeper Protocol complete! The temporal fabric feels much cleaner."
fi

exit 0
