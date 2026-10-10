#!/bin/bash

echo "Welcome to the ApocalypsAI CLI Survival Kit!"
echo "Essential tools pre-loaded for your post-apocalyptic needs."
echo "Type 'list-tools' to see what's available, or just start typing commands."
echo ""

# Function to list tools
list_tools() {
    echo "--- Available Survival Tools ---"
    echo "jq: JSON processor for salvaged data"
    echo "curl: Network requests for faint signals"
    echo "grep: Sift through ancient logs"
    echo "tldr: Quick command reminders (if the network holds)"
    echo "htop: Monitor scavenged server vitals"
    echo "bat: Syntax-highlighted file viewer"
    echo "fzf: Fuzzy finder for navigating forgotten directories"
    echo "--------------------------------"
}

# Check if the first argument is 'list-tools'
if [ "$1" = "list-tools" ]; then
    list_tools
    exit 0
fi

# If no specific command, execute the default command (bash) or the provided command
exec "$@"
