#!/bin/bash

UTIL_PATH="$1"

echo "Checking utility structure at: $UTIL_PATH"

if [ ! -d "$UTIL_PATH" ]; then
    echo "::warning file=$UTIL_PATH::Utility path does not exist. Skipping structure check."
    exit 0 # It's okay if the path doesn't exist, e.g., if a utility is being deleted.
fi

# Check for README.md
if [ ! -f "$UTIL_PATH/README.md" ]; then
    echo "::error file=$UTIL_PATH/README.md::Missing README.md in utility folder."
    exit 1
fi

# Check for src/ directory
if [ ! -d "$UTIL_PATH/src" ]; then
    echo "::error file=$UTIL_PATH/src::Missing src/ directory in utility folder."
    exit 1
fi

# Check for tests/ directory
if [ ! -d "$UTIL_PATH/tests" ]; then
    echo "::error file=$UTIL_PATH/tests::Missing tests/ directory in utility folder."
    exit 1
fi

echo "::notice file=$UTIL_PATH::Utility structure is valid."
exit 0
