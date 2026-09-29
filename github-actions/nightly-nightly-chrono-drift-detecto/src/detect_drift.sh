#!/bin/bash

# Chrono-Drift Detector Script
# Detects files whose filesystem modification time is newer than their last commit time.

REPO_PATH="${1:-.}" # Default to current directory if no path is provided

drift_detected="false"
drift_files=""
drift_count=0

echo "Scanning for chronological drift in: $REPO_PATH"

# Use git ls-files to get all tracked files, including those in submodules if needed.
# -z for null-separated output, safer for filenames with spaces or special characters.
# --full-name to get paths relative to the repository root.
git -C "$REPO_PATH" ls-files -z --full-name | while IFS= read -r -d $'\0' file; do
    # Get last modification time of the file on the filesystem
    # Using stat -c %Y for Linux (GitHub Actions runners are Linux)
    file_mtime=$(stat -c %Y "$REPO_PATH/$file" 2>/dev/null)

    # Get last commit time for the file
    # %ct is committer date, UNIX timestamp
    commit_time=$(git -C "$REPO_PATH" log -1 --format=%ct -- "$file" 2>/dev/null)

    if [[ -z "$file_mtime" || -z "$commit_time" ]]; then
        # Skip if file or commit info cannot be retrieved (e.g., deleted file, new untracked file)
        continue
    fi

    if (( file_mtime > commit_time )); then
        echo "  Drift detected: $file (mtime: $file_mtime, commit_time: $commit_time)"
        drift_detected="true"
        drift_files+="$file\n"
        ((drift_count++))
    fi
done

if [[ "$drift_detected" == "true" ]]; then
    echo "--- Chronological Drift Summary ---"
    echo "Total files with drift: $drift_count"
    echo -e "Files:\n$drift_files"
    echo "---------------------------------"
else
    echo "No chronological drift detected. All timestamps are in harmony."
fi

# Output for GitHub Actions
echo "DRIFT_DETECTED=$drift_detected"
echo "DRIFT_FILES=$drift_files"
