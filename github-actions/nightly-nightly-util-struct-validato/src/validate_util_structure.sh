#!/bin/bash

UTIL_PATH="$1"

echo "--- Validating utility structure for: $UTIL_PATH ---"

# 1. Check if the utility root directory exists
if [ ! -d "$UTIL_PATH" ]; then
  echo "Error: Utility root directory '$UTIL_PATH' does not exist."
  exit 1
fi
echo "✓ Utility root directory exists."

# 2. Check for README.md
if [ ! -f "$UTIL_PATH/README.md" ]; then
  echo "Error: '$UTIL_PATH/README.md' not found."
  exit 1
fi
echo "✓ README.md exists."

# 3. Check for src/ directory
if [ ! -d "$UTIL_PATH/src" ]; then
  echo "Error: '$UTIL_PATH/src' directory not found."
  exit 1
fi
echo "✓ src/ directory exists."

# 4. Check if src/ contains at least one file
if [ -z "$(find "$UTIL_PATH/src" -maxdepth 1 -type f -print -quit)" ]; then
  echo "Error: '$UTIL_PATH/src' directory is empty or contains no files."
  exit 1
fi
echo "✓ src/ directory contains files."

# 5. Check for tests/ directory
if [ ! -d "$UTIL_PATH/tests" ]; then
  echo "Error: '$UTIL_PATH/tests' directory not found."
  exit 1
fi
echo "✓ tests/ directory exists."

# 6. Check if tests/ contains at least one file
if [ -z "$(find "$UTIL_PATH/tests" -maxdepth 1 -type f -print -quit)" ]; then
  echo "Error: '$UTIL_PATH/tests' directory is empty or contains no files."
  exit 1
fi
echo "✓ tests/ directory contains files."

echo "--- Utility structure validation successful! ---"
exit 0
