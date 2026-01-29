#!/bin/bash

# Inputs (passed as environment variables by action.yml)
REQUIRED_BRANCH_PATTERN="${INPUT_REQUIRED_BRANCH_PATTERN:-.*}"
REQUIRED_COMMIT_PHRASE="${INPUT_REQUIRED_COMMIT_PHRASE:-}"
FORBIDDEN_DAY_OF_WEEK="${INPUT_FORBIDDEN_DAY_OF_WEEK:-}"
REQUIRED_ENV_VAR_NAME="${INPUT_REQUIRED_ENV_VAR_NAME:-}"

# GitHub context variables (passed as environment variables by action.yml, mockable for tests)
CURRENT_BRANCH="${GITHUB_REF_NAME:-main}" # Mock rationale: GITHUB_REF_NAME is dynamic, mock for deterministic tests.
LATEST_COMMIT_MESSAGE="${LATEST_COMMIT_MESSAGE:-'Initial commit'}" # Mock rationale: LATEST_COMMIT_MESSAGE is dynamic, mock for deterministic tests.
CURRENT_DAY_OF_WEEK="${CURRENT_DAY_OF_WEEK:-Monday}" # Mock rationale: CURRENT_DAY_OF_WEEK is dynamic, mock for deterministic tests.

REASON=""
ALIGNED=true

# 1. Check forbidden day of week
if [[ -n "$FORBIDDEN_DAY_OF_WEEK" && "$CURRENT_DAY_OF_WEEK" == "$FORBIDDEN_DAY_OF_WEEK" ]]; then
    ALIGNED=false
    REASON="Deployment forbidden on $CURRENT_DAY_OF_WEEK."
fi

# 2. Check branch pattern
if $ALIGNED && [[ ! "$CURRENT_BRANCH" =~ $REQUIRED_BRANCH_PATTERN ]]; then
    ALIGNED=false
    REASON="Branch '$CURRENT_BRANCH' does not match required pattern '$REQUIRED_BRANCH_PATTERN'."
fi

# 3. Check commit message phrase
if $ALIGNED && [[ -n "$REQUIRED_COMMIT_PHRASE" && ! "$LATEST_COMMIT_MESSAGE" =~ "$REQUIRED_COMMIT_PHRASE" ]]; then
    ALIGNED=false
    REASON="Latest commit message does not contain required phrase '$REQUIRED_COMMIT_PHRASE'."
fi

# 4. Check required environment variable
if $ALIGNED && [[ -n "$REQUIRED_ENV_VAR_NAME" ]]; then
    # Check if the variable exists and is 'true'
    VAR_VALUE=$(eval echo "\$$REQUIRED_ENV_VAR_NAME") # Get value of dynamic env var name
    if [[ -z "$VAR_VALUE" || "$VAR_VALUE" != "true" ]]; then
        ALIGNED=false
        REASON="Required environment variable '$REQUIRED_ENV_VAR_NAME' is not set to 'true'."
    fi
fi

if $ALIGNED; then
    echo "::set-output name=alignment_status::aligned"
    echo "::set-output name=reason::Cosmic alignment achieved. Proceed with caution."
    exit 0
else
    echo "::set-output name=alignment_status::misaligned"
    echo "::set-output name=reason::$REASON"
    exit 1 # Indicate failure
fi
