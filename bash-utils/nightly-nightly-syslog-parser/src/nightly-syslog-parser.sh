#!/bin/bash

# nightly-syslog-parser.sh
# A bash script to parse and filter system logs for specific keywords or patterns.

# --- Configuration ---
LOG_FILES=()
KEYWORDS=()
IP_ADDRESSES=()
PATTERNS=()
COUNT_ONLY=false

# --- Functions ---

# Display help message
show_help() {
  echo "Usage: $(basename "$0") [-f <file>] [-k <keyword>] [-i <ip_address>] [-p <pattern>] [-c] [-h]"
  echo "A bash script to parse and filter system logs for specific keywords or patterns."
  echo ""
  echo "Options:"
  echo "  -f <file>        Path to the syslog file to parse. Can be specified multiple times."
  echo "  -k <keyword>     Search for lines containing this keyword (case-insensitive)."
  echo "  -i <ip_address>  Search for lines containing this IP address."
  echo "  -p <pattern>     Search for lines matching this regular expression."
  echo "  -c               Count the number of matching lines instead of displaying them."
  echo "  -h               Display this help message."
  exit 0
}

# Process command-line arguments
while getopts "f:k:i:p:ch" opt;
do
  case "$opt" in
    f) LOG_FILES+=("$OPTARG") ;; 
    k) KEYWORDS+=("$OPTARG") ;; 
    i) IP_ADDRESSES+=("$OPTARG") ;; 
    p) PATTERNS+=("$OPTARG") ;; 
    c) COUNT_ONLY=true ;; 
    h) show_help ;; 
    *)
      echo "Invalid option: -$OPTARG" >&2
      show_help
      exit 1
      ;; 
  esac
done

# --- Input Validation ---
if [ ${#LOG_FILES[@]} -eq 0 ]; then
  echo "Error: No log files specified. Use -f <file>."
  show_help
  exit 1
fi

# Check if any search criteria are provided
if [ ${#KEYWORDS[@]} -eq 0 ] && [ ${#IP_ADDRESSES[@]} -eq 0 ] && [ ${#PATTERNS[@]} -eq 0 ]; then
  echo "Error: No search criteria provided. Use -k, -i, or -p."
  show_help
  exit 1
fi

# --- Core Logic ---

# Build the grep command dynamically
GREP_CMD="grep -E " # Start with extended regex

# Add keyword filters (case-insensitive)
if [ ${#KEYWORDS[@]} -gt 0 ]; then
  for keyword in "${KEYWORDS[@]}"; do
    GREP_CMD+="-i \"$keyword\" "
  done
fi

# Add IP address filters
if [ ${#IP_ADDRESSES[@]} -gt 0 ]; then
  for ip in "${IP_ADDRESSES[@]}"; do
    GREP_CMD+="-F \"$ip\" " # Use -F for fixed string matching for IPs
  done
fi

# Add pattern filters
if [ ${#PATTERNS[@]} -gt 0 ]; then
  for pattern in "${PATTERNS[@]}"; do
    GREP_CMD+="-E \"$pattern\" "
  done
fi

# Add count option if requested
if [ "$COUNT_ONLY" = true ]; then
  GREP_CMD+="-c "
fi

# Execute the grep command on all specified log files

# Temporary file to store combined output for counting
TEMP_OUTPUT=$(mktemp)

for log_file in "${LOG_FILES[@]}"; do
  if [ -f "$log_file" ]; then
    # Append output to temp file
    eval "$GREP_CMD \"$log_file\"" >> "$TEMP_OUTPUT"
  else
    echo "Warning: Log file not found: $log_file" >&2
  fi
done

# If counting, display the count from the temp file
if [ "$COUNT_ONLY" = true ]; then
  # The grep -c option already counts lines, so we just need to sum them up if multiple files were processed
  # However, if grep -c was applied to multiple files, it might output counts per file. We want a total.
  # A simpler approach for total count is to pipe the combined output to wc -l
  # Let's re-evaluate the GREP_CMD to ensure it works for counting.
  # If COUNT_ONLY is true, we should just pipe the combined output to wc -l
  # Let's rebuild the command for counting.
  
  FINAL_CMD=""
  if [ ${#KEYWORDS[@]} -gt 0 ]; then
    for keyword in "${KEYWORDS[@]}"; do
      FINAL_CMD+="-i \"$keyword\" "
    done
  fi
  if [ ${#IP_ADDRESSES[@]} -gt 0 ]; then
    for ip in "${IP_ADDRESSES[@]}"; do
      FINAL_CMD+="-F \"$ip\" "
    done
  fi
  if [ ${#PATTERNS[@]} -gt 0 ]; then
    for pattern in "${PATTERNS[@]}"; do
      FINAL_CMD+="-E \"$pattern\" "
    done
  fi
  
  # Concatenate all log files and pipe to grep with filters, then wc -l
  cat "${LOG_FILES[@]}" 2>/dev/null | grep $FINAL_CMD -c

else
  # If not counting, display the content from the temp file
  cat "$TEMP_OUTPUT"
fi

# Clean up temporary file
rm "$TEMP_OUTPUT"

exit 0
