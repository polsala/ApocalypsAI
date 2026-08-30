#!/bin/bash

WORKFLOW_DIR="${1:-.github/workflows}"
TEMP_FAIL_SIGNAL=$(mktemp)

# Initialize with success (0)
echo "0" > "$TEMP_FAIL_SIGNAL"

echo "Scanning workflows in: $WORKFLOW_DIR"

# Find all YAML files in the workflow directory and process them
find "$WORKFLOW_DIR" -type f -name "*.yml" | while read -r WORKFLOW_FILE; do
    echo "Checking $WORKFLOW_FILE..."
    CONTENT=$(cat "$WORKFLOW_FILE")
    FILE_HAS_ERROR=false

    # Check for the start and end markers of the Oracle Entry block
    if ! echo "$CONTENT" | grep -q "--- Workflow Oracle Entry ---"; then
        echo "::error file=$WORKFLOW_FILE::Missing '--- Workflow Oracle Entry ---' block."
        FILE_HAS_ERROR=true
    fi

    if ! echo "$CONTENT" | grep -q "--- End Workflow Oracle Entry ---"; then
        echo "::error file=$WORKFLOW_FILE::Missing '--- End Workflow Oracle Entry ---' block."
        FILE_HAS_ERROR=true
    fi

    # Only proceed with field checks if the block markers are present to avoid noise
    if ! $FILE_HAS_ERROR; then
        PURPOSE=$(echo "$CONTENT" | grep -E '^# Purpose:' | sed -E 's/^# Purpose: *(.*)/\1/')
        TRIGGER=$(echo "$CONTENT" | grep -E '^# Trigger:' | sed -E 's/^# Trigger: *(.*)/\1/')
        CRITICALITY=$(echo "$CONTENT" | grep -E '^# Criticality:' | sed -E 's/^# Criticality: *(.*)/\1/')
        SURVIVAL_TIP=$(echo "$CONTENT" | grep -E '^# Survival Tip:' | sed -E 's/^# Survival Tip: *(.*)/\1/')

        if [ -z "$PURPOSE" ]; then
            echo "::error file=$WORKFLOW_FILE::'Purpose' field is empty or missing."
            FILE_HAS_ERROR=true
        fi
        if [ -z "$TRIGGER" ]; then
            echo "::error file=$WORKFLOW_FILE::'Trigger' field is empty or missing."
            FILE_HAS_ERROR=true
        fi
        if [ -z "$CRITICALITY" ]; then
            echo "::error file=$WORKFLOW_FILE::'Criticality' field is empty or missing."
            FILE_HAS_ERROR=true
        fi
        if [ -z "$SURVIVAL_TIP" ]; then
            echo "::error file=$WORKFLOW_FILE::'Survival Tip' field is empty or missing."
            FILE_HAS_ERROR=true
        fi
    fi

    # If any error was found for the current file, signal overall failure
    if $FILE_HAS_ERROR; then
        echo "1" > "$TEMP_FAIL_SIGNAL"
    fi
done

# Read the final failure status from the temporary file
SHOULD_FAIL=$(cat "$TEMP_FAIL_SIGNAL")
rm "$TEMP_FAIL_SIGNAL" # Clean up the temporary file

if [ "$SHOULD_FAIL" -eq 1 ]; then
    echo "::error::Workflow Purpose Oracle detected issues. Please update your workflows."
    exit 1
else
    echo "::notice::All workflows are blessed by the Workflow Purpose Oracle. Documentation is in order!"
    exit 0
fi
