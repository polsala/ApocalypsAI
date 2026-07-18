#!/bin/bash

# Test script for Nightly Docker Environment Manager

set -e # Exit immediately if a command exits with a non-zero status.

echo "Running environment manager tests..."

# Test Git
if ! command -v git &> /dev/null; then
    echo "Error: git command not found!"
    exit 1
fi
echo "Git is installed and accessible."

# Test Curl
if ! command -v curl &> /dev/null; then
    echo "Error: curl command not found!"
    exit 1
fi
echo "Curl is installed and accessible."

# Test Vim
if ! command -v vim &> /dev/null; then
    echo "Error: vim command not found!"
    exit 1
fi
echo "Vim is installed and accessible."

# Test Nano
if ! command -v nano &> /dev/null; then
    echo "Error: nano command not found!"
    exit 1
fi
echo "Nano is installed and accessible."

# Test Wget
if ! command -v wget &> /dev/null; then
    echo "Error: wget command not found!"
    exit 1
fi
echo "Wget is installed and accessible."

# Test Python
if ! command -v python &> /dev/null; then
    echo "Error: python command not found!"
    exit 1
fi
echo "Python is installed and accessible."

# Mock rationale: These tests are deterministic and offline as they only rely on the presence and basic executability of tools within the containerized environment, which is built from a static Dockerfile.

echo "All environment manager tests passed successfully!"
exit 0
