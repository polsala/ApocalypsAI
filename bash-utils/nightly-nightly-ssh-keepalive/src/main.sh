#!/usr/bin/env bash
set -euo pipefail

INTERVAL=300
PORT=22
HOSTS=()

print_usage() {
  echo "Usage: $0 [-i interval] [-p port] [-f file] host..."
  exit 1
}

while getopts ":i:p:f:" opt; do
  case $opt in
    i) INTERVAL=$OPTARG ;;
    p) PORT=$OPTARG ;;
    f)
      while IFS= read -r line; do
        [[ -n $line ]] && HOSTS+=("$line")
      done < "$OPTARG"
      ;;
    *) print_usage ;;
  esac
done
shift $((OPTIND -1))

# Remaining arguments are hosts
for host in "$@"; do
  HOSTS+=("$host")
done

if [[ ${#HOSTS[@]} -eq 0 ]]; then
  echo "Error: No hosts specified."
  print_usage
fi

FAIL=0

probe_host() {
  local host=$1
  if nc -z -w5 "$host" "$PORT"; then
    echo "[$(date +%T)] $host:$PORT is reachable"
  else
    echo "[$(date +%T)] $host:$PORT is unreachable"
    FAIL=1
  fi
}

for host in "${HOSTS[@]}"; do
  probe_host "$host"
done

exit $FAIL
