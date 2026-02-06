#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: $0 [options] <directory>

Options:
  -t <size>   Size threshold (e.g., 10M, 500K). Default: 10M.
  -m          Move files to an archive/ subdirectory (dry‑run by default).
  -h          Show this help message.
EOF
}

# Default values
threshold="10M"
move=false

while getopts ":t:mh" opt; do
  case $opt in
    t) threshold=$OPTARG ;;
    m) move=true ;;
    h) usage ; exit 0 ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ; usage ; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2 ; usage ; exit 1 ;;
  esac
done
shift $((OPTIND-1))

if [ $# -ne 1 ]; then
  echo "Directory argument required." >&2
  usage
  exit 1
fi

target_dir=$1
if [ ! -d "$target_dir" ]; then
  echo "Error: $target_dir is not a directory." >&2
  exit 1
fi

# Find files larger than the threshold
mapfile -t large_files < <(find "$target_dir" -type f -size +"$threshold" 2>/dev/null)

if [ ${#large_files[@]} -eq 0 ]; then
  echo "No files larger than $threshold found in $target_dir."
  exit 0
fi

for file in "${large_files[@]}"; do
  rel_path=${file#"$target_dir"/}
  echo "🔮 $rel_path is a massive relic (> $threshold)."
  if $move; then
    dest_dir="$target_dir/archive/$(dirname "$rel_path")"
    mkdir -p "$dest_dir"
    mv "$file" "$dest_dir/"
    echo "✨ Moved to $dest_dir"
  fi
done
