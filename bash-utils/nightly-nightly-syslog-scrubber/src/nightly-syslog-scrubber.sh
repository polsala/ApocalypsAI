#!/bin/bash

# Default configuration
DEFAULT_KEYWORDS="ERROR CRITICAL FAILURE WARNING ALERT"
DEFAULT_IP_MASK="[IP_REDACTED]"
DEFAULT_USER_MASK="[USER_REDACTED]"

# Load configuration from environment variables or use defaults
KEYWORDS=${SYSLOG_SCRUBBER_KEYWORDS:-$DEFAULT_KEYWORDS}
IP_MASK=${SYSLOG_SCRUBBER_IP_MASK:-$DEFAULT_IP_MASK}
USER_MASK=${SYSLOG_SCRUBBER_USER_MASK:-$DEFAULT_USER_MASK}
TIMESTAMP_FORMAT=${SYSLOG_SCRUBBER_TIMESTAMP_FORMAT}

# Function to highlight keywords
highlight_keywords() {
    local line="$1"
    local highlighted_line="$line"
    for keyword in $KEYWORDS; do
        # Use ANSI escape codes for bold red for critical keywords, bold yellow for others
        if [[ "$keyword" == "ERROR" || "$keyword" == "CRITICAL" || "$keyword" == "FAILURE" ]]; then
            highlighted_line=$(echo "$highlighted_line" | sed -E "s/($keyword)/\x1b[1;31m\1\x1b[0m/g")
        else
            highlighted_line=$(echo "$highlighted_line" | sed -E "s/($keyword)/\x1b[1;33m\1\x1b[0m/g")
        fi
    done
    echo "$highlighted_line"
}

# Function to reformat timestamp if requested
reformat_timestamp() {
    local line="$1"
    local timestamp_part="$(echo "$line" | grep -oE '^[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?Z?|[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}' | head -n 1)"
    if [[ -n "$timestamp_part" ]]; then
        local reformatted_ts=$(date -d "$timestamp_part" "$TIMESTAMP_FORMAT" 2>/dev/null)
        if [[ -n "$reformatted_ts" ]]; then
            echo "$line" | sed "s/$timestamp_part/$reformatted_ts/"
        else
            echo "$line"
        fi
    else
        echo "$line"
    fi
}

# Process each line of input
while IFS= read -r line;
do
    # 1. Redact IP addresses (IPv4 and IPv6)
    scrubbed_line=$(echo "$line" | sed -E "s/([0-9]{1,3}\.){3}[0-9]{1,3}/$IP_MASK/g")
    scrubbed_line=$(echo "$scrubbed_line" | sed -E "s/([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}/$IP_MASK/g") # Basic IPv6
    scrubbed_line=$(echo "$scrubbed_line" | sed -E "s/([0-9a-fA-F]{1,4}:){1,7}:[0-9a-fA-F]{1,4}/$IP_MASK/g") # Compressed IPv6

    # 2. Redact common usernames (simple heuristic: word followed by @ or ending with a common user suffix)
    scrubbed_line=$(echo "$scrubbed_line" | sed -E "s/([a-zA-Z0-9_.-]+)@/$USER_MASK@/g")
    scrubbed_line=$(echo "$scrubbed_line" | sed -E "s/(user|admin|root|guest|sys|daemon|nobody)([[:space:]]|$)/$USER_MASK\2/g")

    # 3. Reformat timestamp if requested
    if [[ -n "$TIMESTAMP_FORMAT" ]]; then
        scrubbed_line=$(reformat_timestamp "$scrubbed_line")
    fi

    # 4. Highlight keywords
    final_line=$(highlight_keywords "$scrubbed_line")

    # Output the processed line
    echo "$final_line"

done
