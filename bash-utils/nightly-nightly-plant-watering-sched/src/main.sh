#!/usr/bin/env bash
set -euo pipefail

# Configuration via environment variables
DATA_FILE="${PLANT_DATA_FILE:-$HOME/.plant_watering}"
INTERVAL_DAYS="${INTERVAL_DAYS:-7}"
CURRENT_DATE="${CURRENT_DATE:-$(date +%Y-%m-%d)}"

# Helper: calculate whole days between two ISO dates (YYYY-MM-DD)
function days_between() {
  local start="$1"
  local end="$2"
  local start_ts=$(date -d "$start" +%s)
  local end_ts=$(date -d "$end" +%s)
  echo $(( (end_ts - start_ts) / 86400 ))
}

# Record a watering event
if [[ "${1:-}" == "--water" && -n "${2:-}" ]]; then
  plant="$2"
  # Ensure the data file exists
  mkdir -p "$(dirname "$DATA_FILE")"
  tmp=$(mktemp)
  # Remove any existing entry for this plant
  if [[ -f "$DATA_FILE" ]]; then
    grep -v "^${plant}:" "$DATA_FILE" > "$tmp" || true
  else
    > "$tmp"
  fi
  # Append the new record
  echo "${plant}:${CURRENT_DATE}" >> "$tmp"
  mv "$tmp" "$DATA_FILE"
  echo "Recorded watering for $plant on $CURRENT_DATE"
  exit 0
fi

# List plants that need watering
if [[ ! -f "$DATA_FILE" ]]; then
  echo "No plant data found."
  exit 0
fi

while IFS=: read -r plant last_date; do
  # Skip empty lines
  [[ -z "$plant" ]] && continue
  days=$(days_between "$last_date" "$CURRENT_DATE")
  if (( days >= INTERVAL_DAYS )); then
    echo "${plant} needs watering (last watered ${last_date}, ${days} days ago)"
  fi
done < "$DATA_FILE"
