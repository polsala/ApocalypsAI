#!/bin/bash

# Get inputs from environment variables set by the composite action
PR_DESCRIPTION="${PR_DESCRIPTION}"
REQUIRED_PHRASES="${REQUIRED_PHRASES}"

# Split the comma-separated phrases into an array
IFS=',' read -ra PHRASE_ARRAY <<< "$REQUIRED_PHRASES"

AFFIRMATION_FOUND="false"

# Loop through each required phrase and check if it exists in the PR description
for phrase in "${PHRASE_ARRAY[@]}"; do
  # Use [[ ... == *"$substring"* ]] for substring matching in bash
  if [[ "$PR_DESCRIPTION" == *"$phrase"* ]]; then
    AFFIRMATION_FOUND="true"
    break # Found one, no need to check further
  fi
done

# Set the action output
echo "::set-output name=affirmation-found::$AFFIRMATION_FOUND"

# If no affirmation was found, fail the action and provide an error message
if [ "$AFFIRMATION_FOUND" == "false" ]; then
  echo "::error file=action.yml::Pull Request description must contain one of the required phrases: ${REQUIRED_PHRASES}"
  exit 1
fi
