#!/usr/bin/env bash
# nightly-disk-guardian
# Checks root partition usage and prints whimsical messages.

# Default usage threshold (percentage) before warning.
THRESHOLD=${THRESHOLD:-80}

# Function to obtain usage percentage of the root filesystem.
# Returns a number without the trailing % sign.
function get_usage() {
  local usage
  usage=$(df -h / | awk 'NR==2 {gsub("%","",$5); print $5}')
  echo "$usage"
}

# Main entry point.
function main() {
  local usage
  # Allow tests to override the data source by defining get_df.
  if declare -f get_df >/dev/null; then
    usage=$(get_df)
  else
    usage=$(get_usage)
  fi

  if (( usage > THRESHOLD )); then
    cat <<'EOF'
   _____  _               _   _             
  |  __ \| |             | | (_)            
  | |  | | |__   ___  ___| |_ _  ___  _ __  
  | |  | | '_ \ / _ \/ __| __| |/ _ \| '_ \ 
  | |__| | | | |  __/ (__| |_| | (_) | | | |
  |_____/|_| |_|\___|\___|\__|_|\___/|_| |_|
                                            
Your disk is bursting at ${usage}%! Time to clean up!
EOF
    return 1
  else
    echo "All is calm. Disk usage at ${usage}%."
    return 0
  fi
}

# If the script is executed directly, run main.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
