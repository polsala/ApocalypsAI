#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: disk-guardian [-t <percent>] <path>
  -t <percent>  Usage threshold (1-100). Default is 80.
  -h            Show this help message.
EOF
}

threshold=80
while getopts ":t:h" opt; do
  case $opt in
    t)
      threshold=$OPTARG
      ;;
    h)
      usage
      exit 0
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))

if [[ $# -ne 1 ]]; then
  echo "Error: path argument required." >&2
  usage
  exit 1
fi

target_path=$1

# Get disk usage percentage for the given path using df -P (POSIX output)
df_output=$(df -P "$target_path" | tail -1)
# Expected columns: Filesystem 1024-blocks Used Available Capacity Mounted on
# Capacity column ends with %
usage_percent=$(echo "$df_output" | awk '{print $5}' | tr -d '%')

if ! [[ "$usage_percent" =~ ^[0-9]+$ ]]; then
  echo "Failed to parse disk usage." >&2
  exit 1
fi

if (( usage_percent >= threshold )); then
  cat <<EOF
⚔️  Disk Guardian warns! ⚔️
   Your $target_path is at ${usage_percent}% capacity.
   Consider cleaning up some space.
   (╯°□°)╯︵ ┻━┻
EOF
  exit 0
else
  echo "✅ $target_path usage is ${usage_percent}% (below ${threshold}%). All clear."
  exit 0
fi
