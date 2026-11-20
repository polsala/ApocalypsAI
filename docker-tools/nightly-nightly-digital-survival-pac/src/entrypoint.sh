#!/bin/bash

# Whimsical welcome message
echo "---------------------------------------------------"
echo "  Welcome to the Nightly Digital Survival Pack!  "
echo "  May your bytes be ever resilient.             "
echo "---------------------------------------------------"
echo ""
echo "Available tools: bash, curl, jq, grep, awk, sed, git, htop, nmap, ssh, rsync, vim"
echo ""

# Execute the command passed to the container, or fall back to bash
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    exec bash
fi
