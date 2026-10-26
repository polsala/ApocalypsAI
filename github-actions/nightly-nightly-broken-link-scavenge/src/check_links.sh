#!/bin/bash

# Nightly Broken Link Scavenger - Core Script

# This script scans markdown files for external HTTP/HTTPS links,
# checks their status, and reports any broken ones.

# Usage: check_links.sh <scan_path> <ignore_patterns_string>
# Output: A newline-separated list of broken links if any, empty string otherwise.
# Format: [HTTP_CODE] <URL> (found in <FILE_PATH>)

SCAN_PATH="${1:-.}"
IGNORE_PATTERNS_STRING="${2:-}"

# Convert newline-separated ignore patterns into a bash array
IFS=$'\n' read -d '' -r -a IGNORE_PATTERNS_ARRAY <<< "$IGNORE_PATTERNS_STRING"

BROKEN_LINKS_REPORT=""

# Function to check if a URL should be ignored
should_ignore_url() {
  local url="$1"
  for pattern in "${IGNORE_PATTERNS_ARRAY[@]}"; do
    if [[ -n "$pattern" && "$url" =~ $pattern ]]; then
      return 0 # True, ignore
    fi
  done
  return 1 # False, do not ignore
}

# Function to fetch HTTP status code (can be mocked for testing)
# Mock rationale: For deterministic and offline testing, the 'curl' command
# is mocked in the test environment. In production, it makes actual network requests.
fetch_url_status() {
  local url="$1"
  # Use 'curl' for actual network requests
  # -s: silent
  # -o /dev/null: discard output
  # -w "%{http_code}": print HTTP status code
  # -m 5: max time 5 seconds
  # -L: follow redirects
  # -I: HEAD request (faster, less data)
  # Fallback to GET if HEAD is not allowed or fails (e.g., some S3 buckets)
  
  # Try HEAD first
  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -m 5 -L -I "$url" 2>/dev/null || true)

  # If HEAD failed or returned 000 (e.g., server doesn't support HEAD or connection issue), try GET
  if [[ -z "$HTTP_CODE" || "$HTTP_CODE" == "000" ]]; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -m 5 -L "$url" 2>/dev/null || true)
  fi

  echo "$HTTP_CODE"
}

export -f fetch_url_status # Export for subshells/mocking

# Find all markdown files and iterate
find "$SCAN_PATH" -type f -name "*.md" | while IFS= read -r md_file;
do
  # Extract all http(s) links from the markdown file
  # Using grep with PCRE for better URL matching
  # Regex: (http|https)://[a-zA-Z0-9./?#&=_-]+ - simplified for common cases
  # More robust regex: https://stackoverflow.com/questions/5717093/check-if-a-javascript-string-is-a-url
  # For simplicity, we'll use a common pattern that covers most cases
  grep -oP '(http|https)://[a-zA-Z0-9\.\/?#&=%_\-]+' "$md_file" | sort -u | while IFS= read -r url;
  do
    if should_ignore_url "$url"; then
      continue
    fi

    status_code=$(fetch_url_status "$url")

    # Check if status code is not 2xx (e.g., 3xx redirects are followed by -L, so we care about final status)
    # Also consider 000 for connection errors or empty responses
    if [[ -n "$status_code" && "$status_code" != "000" && ! "$status_code" =~ ^2[0-9]{2}$ ]]; then
      BROKEN_LINKS_REPORT+="[$status_code] $url (found in $md_file)\n"
    fi
  done
done

# Output the report
echo -e "$BROKEN_LINKS_REPORT"
