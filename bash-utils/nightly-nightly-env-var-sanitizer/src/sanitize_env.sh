#!/usr/bin/env bash

# nightly-env-var-sanitizer
# Redacts sensitive values in .env files.
#
# Usage: sanitize_env.sh [-o output_file] input_file
#   -o output_file   Write sanitized content to the given file (default: stdout)
#   input_file       Path to the .env file to sanitize (required)

set -euo pipefail

# Default values
output=""

# Parse flags
while [[ $# -gt 0 ]]; do
  case "$1" in
    -o)
      if [[ -z "${2-}" ]]; then
        echo "Error: -o requires an argument" >&2
        exit 1
      fi
      output="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: $0 [-o output_file] input_file"
      exit 0
      ;;
    *)
      input_file="$1"
      shift
      ;;
  esac
done

if [[ -z "${input_file-}" ]]; then
  echo "Error: input file is required" >&2
  exit 1
fi

if [[ ! -f "$input_file" ]]; then
  echo "Error: file '$input_file' does not exist" >&2
  exit 1
fi

# Patterns that indicate a secret value
secret_patterns=(
  "*_KEY"
  "*_SECRET"
  "*_TOKEN"
  "*_PASS"
  "*_PASSWORD"
  "*_PWD"
  "*_API_KEY"
  "*_ACCESS_KEY"
  "*_PRIVATE_KEY"
)

# Function to decide if a variable name is secret
is_secret() {
  local var_name="$1"
  for pat in "${secret_patterns[@]}"; do
    if [[ "$var_name" == $pat ]]; then
      return 0
    fi
  done
  return 1
}

# Process the file line‑by‑line
sanitize_line() {
  local line="$1"
  # Preserve comments and empty lines
  if [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]]; then
    echo "$line"
    return
  fi
  # Split on the first '='
  if [[ "$line" =~ ^([^=[:space:]]+)[[:space:]]*=[[:space:]]*(.*)$ ]]; then
    local name="${BASH_REMATCH[1]}"
    local value="${BASH_REMATCH[2]}"
    if is_secret "$name"; then
      echo "${name}=***REDACTED***"
    else
      echo "$line"
    fi
  else
    # Lines that don't match KEY=VALUE are passed through unchanged
    echo "$line"
  fi
}

# Main loop
output_content=""
while IFS= read -r line || [[ -n "$line" ]]; do
  sanitized=$(sanitize_line "$line")
  output_content+="$sanitized"
  output_content+=$'\n'
 done < "$input_file"

# Write to the appropriate destination
if [[ -n "$output" ]]; then
  printf "%s" "$output_content" > "$output"
else
  printf "%s" "$output_content"
fi
