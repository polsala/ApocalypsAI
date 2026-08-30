#!/usr/bin/env bash
set -euo pipefail

# Default data file (can be overridden with PLANT_DATA_FILE env var)
DATA_FILE="${PLANT_DATA_FILE:-${HOME}/.plant_watering.csv}"

# Allow overriding the current date for testing via DATE_OVERRIDE env var (YYYY-MM-DD)
CURRENT_DATE="${DATE_OVERRIDE:-$(date +%F)}"

usage() {
  cat <<'EOF'
plant-watering-reminder - track when to water your houseplants

Usage:
  reminder.sh [options] [plant_name]

Options:
  --list               List all plants with next watering date
  --water <plant>      Mark <plant> as watered today
  -h, --help           Show this help
If a plant name is given without options, the script checks if it needs watering.
EOF
  exit 1
}

# Ensure data file exists
if [[ ! -f "$DATA_FILE" ]]; then
  echo "Data file not found at $DATA_FILE" >&2
  exit 1
fi

# Parse CSV into associative arrays
declare -A last_watered interval

while IFS=, read -r name last interval_days; do
  [[ -z "$name" ]] && continue
  last_watered["$name"]="$last"
  interval["$name"]="$interval_days"
done < "$DATA_FILE"

date_to_seconds() {
  date -d "$1" +%s
}

days_between() {
  local start=$1 end=$2
  echo $(( ( $(date_to_seconds "$end") - $(date_to_seconds "$start") ) / 86400 ))
}

needs_watering() {
  local name=$1
  local last="${last_watered[$name]}"
  local int="${interval[$name]}"
  local days_since=$(days_between "$last" "$CURRENT_DATE")
  (( days_since >= int ))
}

list_plants() {
  for name in "${!last_watered[@]}"; do
    local last="${last_watered[$name]}"
    local int="${interval[$name]}"
    local next_date=$(date -d "$last +$int days" +%F)
    echo "$name: next watering on $next_date"
  done
}

mark_watered() {
  local target=$1
  if [[ -z "${last_watered[$target]:-}" ]]; then
    echo "Plant '$target' not found in $DATA_FILE" >&2
    exit 1
  fi
  # Update the CSV in-place
  local tmp=$(mktemp)
  while IFS=, read -r name last int; do
    if [[ "$name" == "$target" ]]; then
      echo "$name,$CURRENT_DATE,$int" >> "$tmp"
    else
      echo "$name,$last,$int" >> "$tmp"
    fi
  done < "$DATA_FILE"
  mv "$tmp" "$DATA_FILE"
  echo "Marked '$target' as watered on $CURRENT_DATE"
}

# Argument parsing
if [[ $# -eq 0 ]]; then
  usage
fi

case "$1" in
  -h|--help) usage ;;
  --list) list_plants; exit 0 ;;
  --water)
    if [[ -z "${2:-}" ]]; then
      echo "Missing plant name for --water" >&2
      exit 1
    fi
    mark_watered "$2"
    exit 0
    ;;
  *)
    plant="$1"
    if [[ -z "${last_watered[$plant]:-}" ]]; then
      echo "Plant '$plant' not found in $DATA_FILE" >&2
      exit 1
    fi
    if needs_watering "$plant"; then
      echo "💧 Plant '$plant' needs watering!"
    else
      echo "✅ Plant '$plant' is fine."
    fi
    ;;
esac
