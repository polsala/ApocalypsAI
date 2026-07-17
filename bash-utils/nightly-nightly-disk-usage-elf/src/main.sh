#!/usr/bin/env bash
# nightly-disk-usage-elf – report disk usage with emojis and an ASCII elf for high usage.

# Default warning threshold (percentage). Can be overridden by setting the THRESHOLD env var.
THRESHOLD=${THRESHOLD:-80}

# Function to print the ASCII elf when any partition exceeds the threshold.
print_elf() {
  cat <<'EOF'
   /\
  /  \
 /____\
 |    |
 |____|
 (\_/)
 ( •_•)
 / >🍎  Time to clean up!
EOF
}

# Flag to indicate whether we printed any warnings.
warning_found=false

# Use df with POSIX output format (-P) and kilobyte units (-k) for reliable parsing.
while IFS= read -r line; do
  # Skip the header line.
  [[ "$line" =~ ^Filesystem ]] && continue

  # Parse the fields.
  filesystem=$(echo "$line" | awk '{print $1}')
  size=$(echo "$line" | awk '{print $2}')
  used=$(echo "$line" | awk '{print $3}')
  avail=$(echo "$line" | awk '{print $4}')
  usep=$(echo "$line" | awk '{print $5}' | tr -d '%')
  mount=$(echo "$line" | awk '{print $6}')

  if (( usep >= THRESHOLD )); then
    echo -e "⚠️  $mount is at ${usep}%"
    warning_found=true
  else
    echo -e "✅  $mount is at ${usep}%"
  fi
done < <(df -P -k)

# If any warning was emitted, show the elf.
if $warning_found; then
  print_elf
fi
