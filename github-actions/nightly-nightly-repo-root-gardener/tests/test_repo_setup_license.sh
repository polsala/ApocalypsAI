#!/bin/bash
# Mock rationale: This script creates a controlled, deterministic file system state
# for the GitHub Action to operate on, simulating a repository without needing
# actual Git operations or external dependencies.

# Clean up previous test runs
rm -rf README.md LICENSE CONTRIBUTING.md MISSING.md .DS_Store temp_config.bak src/

# Create common required files
echo "# My Awesome Project" > README.md
echo "MIT License" > LICENSE

# Create a source file without a license header
mkdir -p src
echo "def hello():" > src/main.py
echo "    print('Hello, world!')" >> src/main.py

# Create a source file with a license header (should pass)
echo "# Copyright (c) 2023 ApocalypsAI" > src/another.py
echo "def goodbye():" >> src/another.py
echo "    print('Goodbye!')" >> src/another.py
