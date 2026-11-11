#!/usr/bin/env bash
set -euo pipefail

# Function to obtain root filesystem usage percentage (without the % sign)
get_root_usage() {
    df -h / | awk 'NR==2 {gsub("%","",$5); print $5}'
}

# Array of apocalypse‑themed messages
APOC_MESSAGES=(
    "The world is ending!"
    "All hope is lost!"
    "The sky is falling!"
    "Rocks are raining!"
    "The servers are melting!"
)

# Pick a random message from the array
random_message() {
    local idx=$((RANDOM % ${#APOC_MESSAGES[@]}))
    echo "${APOC_MESSAGES[$idx]}"
}

# Main entry point – can be called directly or sourced for testing
main() {
    local threshold=${1:-80}
    local usage
    usage=$(get_root_usage)

    if (( usage > threshold )); then
        local msg
        msg=$(random_message)
        echo "⚠️  Disk usage at ${usage}% – ${msg}"
        cat <<'EOF'
   ____
  /____\   *BOOM*
EOF
        return 1
    else
        echo "✅ Disk usage at ${usage}% – All is calm."
        return 0
    fi
}

# Execute main only when the script is run directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
    exit $?
fi
