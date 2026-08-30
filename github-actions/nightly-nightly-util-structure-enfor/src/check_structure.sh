#!/bin/bash

# This script checks if newly added utility directories adhere to the ApocalypsAI structure:
# - Must contain a README.md file
# - Must contain a tests/ subdirectory

# Arguments:
# $1: Space-separated string of newly added file paths (e.g., "path/to/file1 path/to/file2")
# $2: Comma-separated string of parent directories to check (e.g., "utils/,python-utils/")

NEW_FILES_STR="$1"
CHECK_PATHS_STR="$2"

# Convert space-separated string to array
IFS=' ' read -r -a NEW_FILES_ARRAY <<< "$NEW_FILES_STR"

# Convert comma-separated string to array, ensuring each path ends with a slash
IFS=',' read -r -a CHECK_PATHS_RAW_ARRAY <<< "$CHECK_PATHS_STR"
CHECK_PATHS_ARRAY=()
for path in "${CHECK_PATHS_RAW_ARRAY[@]}"; do
    [[ "$path" != */ ]] && path="${path}/"
    CHECK_PATHS_ARRAY+=("$path")
done

declare -A new_util_dirs # Associative array to store unique utility root directories

# Iterate through new files to identify unique new utility directories
for file_path in "${NEW_FILES_ARRAY[@]}"; do
    # Skip if file_path is empty (can happen with empty NEW_FILES_STR)
    [[ -z "$file_path" ]] && continue

    dir_name=$(dirname "$file_path")
    
    # Check if this directory is a potential utility directory within a classifier path
    for check_path in "${CHECK_PATHS_ARRAY[@]}"; do
        if [[ "$dir_name" == "$check_path"* ]]; then
            # Extract the utility's root directory (e.g., python-utils/my-util)
            # This assumes the structure is <classifier-path>/<util_name>/...
            relative_path="${dir_name#$check_path}"
            
            # If relative_path contains a slash, it means we're in a subdirectory of the util
            # The util_root_dir is <check_path><first_segment_of_relative_path>
            if [[ "$relative_path" == */* ]]; then
                util_root_dir="${check_path}${relative_path%%/*}"
            else
                # The file is directly in <classifier-path>/<util_name>
                util_root_dir="${check_path}${relative_path}"
            fi
            
            # Add to unique list if it's a non-empty, valid utility root directory
            if [[ -n "$util_root_dir" && "$util_root_dir" != "$check_path" ]]; then # Ensure it's not just the classifier path itself
                new_util_dirs["$util_root_dir"]=1
            fi
            break # Found a matching check_path for this file, move to next file
        fi
    done
done

errors=0

# Perform checks for each identified new utility directory
for util_dir in "${!new_util_dirs[@]}"; do
    echo "Checking new utility directory: $util_dir"
    
    if [[ ! -f "$util_dir/README.md" ]]; then
        echo "::error file=$util_dir/README.md::Error: Directory '$util_dir' is missing README.md"
        errors=$((errors + 1))
    fi
    
    if [[ ! -d "$util_dir/tests" ]]; then
        echo "::error file=$util_dir/tests::Error: Directory '$util_dir' is missing a 'tests/' subdirectory"
        errors=$((errors + 1))
    fi
done

if [[ "$errors" -gt 0 ]]; then
    echo "::error::Utility structure check failed with $errors errors."
    exit 1
else
    echo "All new utility directories adhere to the structure requirements."
fi
