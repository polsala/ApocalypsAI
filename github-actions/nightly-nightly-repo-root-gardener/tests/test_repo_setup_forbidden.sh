#!/bin/bash
# Mock rationale: This script creates a controlled, deterministic file system state
# for the GitHub Action to operate on, simulating a repository without needing
# actual Git operations or external dependencies.

# Clean up previous test runs
rm -rf README.md LICENSE CONTRIBUTING.md MISSING.md .DS_Store temp_config.bak src/

# Create common required files
echo "# My Awesome Project" > README.md
echo "MIT License" > LICENSE

# Create a forbidden file
echo "This is a forbidden file." > .DS_Store
