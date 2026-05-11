#!/bin/bash
set -e

echo "Welcome to the Temporal Toolkit Tesseract!"
echo "Essential tools at your fingertips. May your timelines be stable."
echo ""
echo "Available tools: git, curl, wget, jq, yq, vim, tmux, htop, net-tools, ping, ansible, terraform, kubectl, aws"
echo ""

# If no arguments are provided, start an interactive bash shell
if [ "$#" -eq 0 ]; then
    exec bash
else
    # Otherwise, execute the provided command
    exec "$@"
fi
