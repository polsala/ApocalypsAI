#!/usr/bin/env bash

set -e

show_help() {
  cat <<'EOF'
Usage: clean_apt_cache.sh [-n] [-h]

Options:
  -n    Dry run – show the apt-get clean command without executing it.
  -h    Show this help message.
EOF
}

DRY_RUN=0

while getopts ":nh" opt; do
  case $opt in
    n) DRY_RUN=1 ;;
    h) show_help; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2; show_help; exit 1 ;;
  esac
done

CMD="sudo apt-get clean"

if [[ $DRY_RUN -eq 1 ]]; then
  echo "Would run: $CMD"
  exit 0
fi

if [[ -n "$TEST_MODE" ]]; then
  echo "Mock cleaning APT cache (TEST_MODE enabled)."
  exit 0
fi

echo "Executing: $CMD"
$CMD
