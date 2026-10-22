#!/bin/bash

# Default output format
OUTPUT_FORMAT="[%timestamp%] %hostname% %process%: %message%"

# Function to display help message
show_help() {
    echo "Usage: $(basename "$0") [OPTIONS] <log_file>"
    echo ""
    echo "A whimsical yet useful bash utility to parse and filter syslog messages."
    echo ""
    echo "Options:"
    echo "  -p, --pattern <regex>     The regular expression pattern to search for in syslog messages."
    echo "  -o, --output-format <format> The output format string. Available placeholders:"
    echo "                            %timestamp%, %hostname%, %process%, %message%."
    echo "                            Default: \"%timestamp% %hostname% %process%: %message%\"
    echo "  -h, --help                Display this help message."
    echo ""
    echo "Examples:"
    echo "  $(basename "$0") -p \"error\" /var/log/syslog"
    echo "  $(basename "$0") -p \"sshd\" -o \"%timestamp% %message%\" /var/log/syslog"
}

# Parse command-line options
while [[ "$#" -gt 0 ]]; do
    key="$1"
    case $key in
        -p|--pattern)
        PATTERN="$2"
        shift # past argument
        shift # past value
        ;;
        -o|--output-format)
        OUTPUT_FORMAT="$2"
        shift # past argument
        shift # past value
        ;;
        -h|--help)
        show_help
        exit 0
        ;;
        *)
        # Assume the last argument is the log file
        LOG_FILE="$1"
        shift # past argument
        ;;
    esac
done

# Check if log file is provided
if [ -z "$LOG_FILE" ]; then
    echo "Error: Log file not specified."
    show_help
    exit 1
fi

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found."
    exit 1
fi

# Process the log file
while IFS= read -r line || [[ -n "$line" ]]; do
    # Extract fields using awk (common syslog format)
    # This is a basic parsing, more robust parsing might be needed for different syslog formats
    timestamp=$(echo "$line" | awk '{print $1, $2, $3}')
    hostname=$(echo "$line" | awk '{print $4}')
    # Attempt to find process name, which can be tricky if it's not the 5th field
    # This is a simplified approach, assuming process name is after hostname and before message
    # A more robust solution might involve regex matching on the whole line
    process=$(echo "$line" | awk '{for(i=5; i<=NF; i++) if ($i ~ /^[a-zA-Z0-9_-]+(\[[0-9]+\])?(:)?$/) {print $i; exit}}')
    # If process is not found in the expected format, try to get the first word after hostname
    if [ -z "$process" ]; then
        process=$(echo "$line" | awk '{print $5}')
    fi
    # The rest of the line is the message
    message=$(echo "$line" | cut -d' ' -f6-)

    # Apply pattern if specified
    if [ -n "$PATTERN" ]; then
        if ! echo "$line" | grep -qE "$PATTERN"; then
            continue # Skip if pattern doesn't match
        fi
    fi

    # Format the output
    formatted_line="$OUTPUT_FORMAT"
    formatted_line=${formatted_line//%timestamp%/$timestamp}
    formatted_line=${formatted_line//%hostname%/$hostname}
    formatted_line=${formatted_line//%process%/$process}
    formatted_line=${formatted_line//%message%/$message}

    echo "$formatted_line"

done < "$LOG_FILE"
