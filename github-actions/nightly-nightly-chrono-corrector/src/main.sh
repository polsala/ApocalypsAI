#!/bin/bash

# Get inputs from environment variables set by the composite action
GITHUB_TOKEN="$INPUT_GITHUB_TOKEN"
SCAN_PATHS="$INPUT_SCAN_PATHS"
CURRENT_YEAR="$INPUT_CURRENT_YEAR"

# If current-year input is not provided, determine it dynamically
if [ -z "$CURRENT_YEAR" ]; then
  CURRENT_YEAR=$(date +%Y)
fi

PREVIOUS_YEAR=$((CURRENT_YEAR - 1))
ANOMALIES_FOUND="false"
REPORT_LINES=() # Array to store report lines

REPORT_LINES+=("### 🕰️ Nightly Chrono-Corrector Report 🕰️")
REPORT_LINES+=("")
REPORT_LINES+=("The Chrono-Corrector has been diligently scanning the timelines of your repository for temporal discrepancies.")
REPORT_LINES+=("")

IFS=',' read -ra ADDR <<< "$SCAN_PATHS"
for path in "${ADDR[@]}"; do
  # Trim whitespace from path
  path=$(echo "$path" | xargs)
  if [ -f "$path" ]; then
    if grep -q "$PREVIOUS_YEAR" "$path"; then
      ANOMALIES_FOUND="true"
      REPORT_LINES+=("* **File: \`$path\`**: Detected an outdated year (\`$PREVIOUS_YEAR\`). Consider updating to \`$CURRENT_YEAR\`.")
    fi
  elif [ -d "$path" ]; then
    # If it's a directory, scan files within it
    find "$path" -type f -print0 | while IFS= read -r -d $'\0' file; do
      if grep -q "$PREVIOUS_YEAR" "$file"; then
        ANOMALIES_FOUND="true"
        REPORT_LINES+=("* **File: \`$file\`**: Detected an outdated year (\`$PREVIOUS_YEAR\`). Consider updating to \`$CURRENT_YEAR\`.")
      fi
    done
  fi
done

if [ "$ANOMALIES_FOUND" == "false" ]; then
  REPORT_LINES+=("No temporal anomalies (outdated year references) were detected. The timeline is stable. ✨")
fi

# Join report lines with newlines
FINAL_REPORT=$(IFS=$'\n'; echo "${REPORT_LINES[*]}")

echo "anomalies-found=$ANOMALIES_FOUND" >> "$GITHUB_OUTPUT"
echo "report<<EOF" >> "$GITHUB_OUTPUT"
echo "$FINAL_REPORT" >> "$GITHUB_OUTPUT"
echo "EOF" >> "$GITHUB_OUTPUT"
