#!/usr/bin/env bash

# nightly-env-var-sanitizer
# Scans environment variables and redacts values of likely secret variables.
# Supports optional output to a file.

# Patterns that indicate a variable may contain a secret (case‑insensitive)
patterns=("KEY" "TOKEN" "PASS" "SECRET" "PWD" "CRED")

output_file=""

# Parse options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--output)
      output_file="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Function to decide if a variable name looks secrety
is_secret() {
  local var_name="$1"
  for pat in "${patterns[@]}"; do
    if [[ "$var_name" =~ $pat ]]; then
      return 0
    fi
  done
  return 1
}

result=""

# Iterate over environment variables
while IFS='=' read -r name value; do
  if is_secret "$name"; then
    result+="${name}=[REDACTED]\n"
  else
    result+="${name}=${value}\n"
  fi
done < <(env)

if [[ -n "$output_file" ]]; then
  printf "%b" "$result" > "$output_file"
else
  printf "%b" "$result"
fi

exit 0
