#!/usr/bin/env bash
# nightly-ramen-noodle-timer
# Determines cooking time for various noodle types and optionally waits.

set -euo pipefail

# Mapping of noodle types to cooking minutes
declare -A NOODLE_TIMES=(
  [ramen]=8
  [udon]=12
  [soba]=4
  [spaghetti]=10
  [rice]=18
)

usage() {
  cat <<'EOF'
Usage: $(basename "$0") <noodle-type>
Supported noodle types: ramen, udon, soba, spaghetti, rice
EOF
  exit 1
}

if [[ $# -ne 1 ]]; then
  usage
fi

noodle="${1,,}"  # normalize to lowercase

if [[ -z "${NOODLE_TIMES[$noodle]:-}" ]]; then
  echo "Error: Unknown noodle type '$noodle'."
  usage
fi

minutes=${NOODLE_TIMES[$noodle]}

echo "Recommended cooking time for $noodle: $minutes minute(s)."

# If SKIP_SLEEP is set (any non‑empty value), bypass the actual waiting.
if [[ -z "${SKIP_SLEEP:-}" ]]; then
  echo "Waiting... (press Ctrl+C to abort)"
  sleep $((minutes * 60))
  echo "Done! 🍜"
fi
