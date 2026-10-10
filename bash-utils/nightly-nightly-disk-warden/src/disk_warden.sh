#!/usr/bin/env bash
set -euo pipefail

# Function to get disk usage percent for the root filesystem
get_root_usage() {
  if [[ -n "${MOCK_DF_OUTPUT:-}" ]]; then
    # Mock mode: use provided mock output
    echo "$MOCK_DF_OUTPUT"
  else
    df -h / | awk 'NR==2 {print $5}' | tr -d '%'
  fi
}

# Main logic
main() {
  local threshold="${1:-80}"
  if ! [[ "$threshold" =~ ^[0-9]+$ ]] || (( threshold < 0 || threshold > 100 )); then
    echo "Invalid threshold: $threshold"
    exit 1
  fi

  local usage
  usage=$(get_root_usage)

  if (( usage >= threshold )); then
    # Warning
    echo -e "\e[31m⚠️  Disk usage at ${usage}%! Time to clean up! ⚠️\e[0m"
    cat <<'EOF'
   _______________
  /               \
 |   O       O    |
 |      ^         |
 |    \___/       |
  \_____________/
EOF
    exit 2
  else
    echo -e "\e[32m✅ Disk usage at ${usage}% – all clear.\e[0m"
    exit 0
  fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
