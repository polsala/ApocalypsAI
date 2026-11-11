#!/usr/bin/env bash
# nightly-disk-guardian: monitor root disk usage and warn when low.

THRESHOLD=80

# Get usage percent of root filesystem
usage=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')

if [[ -z "$usage" ]]; then
  echo "Error: could not determine disk usage."
  exit 2
fi

if (( usage > THRESHOLD )); then
  cat <<'EOF'
   .-.      .-.
  (   ).  (   )
 (___(__) (___(__)
  ██████████████
  █   LOW SPACE █
  ██████████████
EOF
  echo "⚠️  Disk usage at ${usage}%! The apocalypse approaches. Clean up some files."
  exit 1
else
  echo "✅ Disk usage at ${usage}% – all is calm."
  exit 0
fi
