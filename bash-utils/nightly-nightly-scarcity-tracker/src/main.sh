#!/usr/bin/env bash
# nightly-scarcity-tracker
# Simple inventory manager for post‑apocalyptic resources.

set -euo pipefail

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INV_FILE="${SCRIPT_DIR}/inventory.txt"

# Ensure inventory file exists
touch "$INV_FILE"

usage() {
  echo "Usage: $0 {add|remove|list} [item] [amount]"
  exit 1
}

add_item() {
  local item=$1
  local amount=$2
  if ! [[ "$amount" =~ ^[0-9]+$ ]]; then
    echo "Amount must be a positive integer"
    exit 1
  fi
  # If item exists, increment; else add line
  if grep -q "^${item}:" "$INV_FILE"; then
    local current
    current=$(grep "^${item}:" "$INV_FILE" | cut -d: -f2)
    local new=$((current + amount))
    sed -i "s/^${item}:.*/${item}: ${new}/" "$INV_FILE"
  else
    echo "${item}: ${amount}" >> "$INV_FILE"
  fi
  echo "Added ${amount} of ${item}"
}

remove_item() {
  local item=$1
  local amount=$2
  if ! [[ "$amount" =~ ^[0-9]+$ ]]; then
    echo "Amount must be a positive integer"
    exit 1
  fi
  if ! grep -q "^${item}:" "$INV_FILE"; then
    echo "Item ${item} not found"
    exit 1
  fi
  local current
  current=$(grep "^${item}:" "$INV_FILE" | cut -d: -f2 | tr -d ' ')
  if (( amount > current )); then
    echo "Cannot remove more than existing amount"
    exit 1
  fi
  local new=$((current - amount))
  if (( new == 0 )); then
    # Remove line
    sed -i "/^${item}:/d" "$INV_FILE"
  else
    sed -i "s/^${item}:.*/${item}: ${new}/" "$INV_FILE"
  fi
  echo "Removed ${amount} of ${item}"
}

list_items() {
  if [[ ! -s "$INV_FILE" ]]; then
    echo "Inventory is empty"
    exit 0
  fi
  cat "$INV_FILE"
}

# Main
if [[ $# -lt 1 ]]; then
  usage
fi

cmd=$1
case "$cmd" in
  add)
    [[ $# -eq 3 ]] || usage
    add_item "$2" "$3"
    ;;
  remove)
    [[ $# -eq 3 ]] || usage
    remove_item "$2" "$3"
    ;;
  list)
    [[ $# -eq 1 ]] || usage
    list_items
    ;;
  *)
    usage
    ;;
esac
