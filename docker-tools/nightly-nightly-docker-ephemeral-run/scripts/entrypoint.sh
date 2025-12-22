#!/bin/bash
set -e

# Configuration
GITHUB_OWNER=${GITHUB_OWNER:-""}
GITHUB_REPO=${GITHUB_REPO:-""}
GITHUB_TOKEN=${GITHUB_TOKEN:-""}
RUNNER_NAME=${RUNNER_NAME:-"$(hostname)"}

# Whimsical exit messages
EXIT_MESSAGES=(
    "Mission accomplished! This runner is now going ghost."
    "Job done! Time to fade into the digital ether."
    "All tasks complete! This runner has fulfilled its destiny."
    "Success! This runner is now obsolete."
    "Task completed! This runner is now retiring to a quiet server farm."
    "Job finished! This runner is now joining the cloud in the sky."
)

# Function to get random exit message
get_exit_message() {
    local count=${#EXIT_MESSAGES[@]}
    local index=$((RANDOM % count))
    echo "${EXIT_MESSAGES[$index]}"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "========================================="
    echo "$(get_exit_message)"
    echo "========================================="
    
    # Unregister runner
    if [ -f "/home/runner/.runner" ]; then
        echo "Unregistering runner..."
        sudo -u runner ./config.sh remove --token "$GITHUB_TOKEN" || true
    fi
    
    # Remove runner files
    rm -rf /home/runner/_work
    
    echo "Cleanup complete. Goodbye!"
}

# Set trap for cleanup
trap cleanup EXIT

# Validate required environment variables
if [ -z "$GITHUB_OWNER" ] || [ -z "$GITHUB_REPO" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: Missing required environment variables."
    echo "Please set GITHUB_OWNER, GITHUB_REPO, and GITHUB_TOKEN."
    exit 1
fi

# Switch to runner user and configure
echo "Configuring GitHub Actions runner..."
sudo -u runner ./config.sh \
    --url "https://github.com/$GITHUB_OWNER/$GITHUB_REPO" \
    --token "$GITHUB_TOKEN" \
    --name "$RUNNER_NAME" \
    --ephemeral \
    --unattended

# Start the runner
echo "Starting ephemeral runner..."
echo "Runner name: $RUNNER_NAME"
echo "Repository: $GITHUB_OWNER/$GITHUB_REPO"
echo "========================================="

# Start the runner and wait for it to complete
sudo -u runner ./run.sh

# If we get here, the runner has completed its job
exit 0
