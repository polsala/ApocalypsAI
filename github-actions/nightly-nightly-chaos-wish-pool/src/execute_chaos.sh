#!/bin/bash
set -euo pipefail

# Mock rationale: Using simple shell scripting for chaos execution
# This keeps it lightweight and easy to extend

SCENARIO="$1"
MAX_DURATION="$2"
GITHUB_TOKEN="$3"

# Parse scenario (simplified YAML parsing)
SCENARIO_NAME=$(echo "$SCENARIO" | grep -o "name: [^"]*" | cut -d' ' -f2 | head -1)
SCENARIO_TYPE=$(echo "$SCENARIO" | grep -o "type: [^"]*" | cut -d' ' -f2 | head -1)
DURATION=$(echo "$SCENARIO" | grep -o "duration: [0-9]*" | cut -d' ' -f2 | head -1)

# Use max duration if not specified
if [ -z "$DURATION" ]; then
  DURATION="$MAX_DURATION"
fi

echo "Executing chaos scenario: $SCENARIO_NAME ($SCENARIO_TYPE) for $DURATION seconds"

case "$SCENARIO_TYPE" in
  "branch-rename")
    NEW_NAME=$(echo "$SCENARIO" | grep -o "new_name: [^"]*" | cut -d' ' -f2 | head -1)
    if [ -n "$NEW_NAME" ]; then
      echo "Renaming branch to whimsical name: $NEW_NAME"
      # In real implementation, this would use GitHub API
      echo "# Mock: Would rename branch to $NEW_NAME for $DURATION seconds"
    fi
    ;;
  "file-shuffle")
    echo "Shuffling files around for $DURATION seconds"
    # Mock file operations
    echo "# Mock: Would temporarily move files around"
    ;;
  "commit-spree")
    echo "Creating whimsical commits for $DURATION seconds"
    # Mock commit creation
    echo "# Mock: Would create funny commits"
    ;;
  "emoji-blast")
    echo "Spreading emoji chaos for $DURATION seconds"
    # Mock emoji injection
    echo "# Mock: Would inject playful emojis"
    ;;
  "")
    echo "Warning: No scenario type specified for $SCENARIO_NAME"
    echo "# Mock: No action taken"
    ;;
  *)
    echo "Unknown scenario type: $SCENARIO_TYPE"
    echo "Available types: branch-rename, file-shuffle, commit-spree, emoji-blast"
    exit 1
    ;;
esac

# Schedule cleanup after duration (in real implementation)
echo "Cleanup would be scheduled for $DURATION seconds later"
echo "Scenario completed: $SCENARIO_NAME"

# Return success
echo "## 🎉 Chaos Executed Successfully!"
echo "Scenario: $SCENARIO_NAME"
echo "Duration: $DURATION seconds"
echo "Type: $SCENARIO_TYPE"
