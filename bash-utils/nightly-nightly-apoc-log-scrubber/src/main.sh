#!/bin/bash

# Default configuration file path
DEFAULT_CONFIG="./config/default.conf"

# Function to display usage information
usage() {
    echo "Usage: $0 <input_log_file> <output_log_file> [config_file]"
    echo "  <input_log_file>: Path to the log file to scrub."
    echo "  <output_log_file>: Path to save the scrubbed log file."
    echo "  [config_file]: Optional path to a custom configuration file."
    exit 1
}

# Check if input and output files are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    usage
fi

INPUT_LOG="$1"
OUTPUT_LOG="$2"
CONFIG_FILE="${3:-$DEFAULT_CONFIG}"

# Check if input log file exists
if [ ! -f "$INPUT_LOG" ]; then
    echo "Error: Input log file '$INPUT_LOG' not found."
    exit 1
fi

# Check if configuration file exists, use default if not specified and default doesn't exist
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Warning: Configuration file '$CONFIG_FILE' not found. Using default patterns."
    # Ensure default config exists for the warning to be meaningful
    if [ ! -f "$DEFAULT_CONFIG" ]; then
        echo "Error: Default configuration file '$DEFAULT_CONFIG' also not found. Cannot proceed."
        exit 1
    fi
    CONFIG_FILE="$DEFAULT_CONFIG"
fi

# Create output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_LOG")
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

# Scrub the log file
# Use sed to read patterns from the config file and apply them
# -E enables extended regular expressions
# -e allows multiple expressions
# The loop reads each non-comment line from the config file and adds it as a sed -e expression
SED_EXPRESSIONS=""
while IFS= read -r line || [[ -n "$line" ]]; do
    # Skip empty lines and comments
    if [[ -n "$line" && ! "$line" =~ ^# ]]; then
        # Escape backslashes and quotes for sed command
        ESCAPED_LINE=$(echo "$line" | sed 's/\/\\\//g' | sed 's/"/\\"/g')
        SED_EXPRESSIONS+=" -e 's/$ESCAPED_LINE/REDACTED/g'"
    fi
done < "$CONFIG_FILE"

# Execute sed with all collected expressions
# Using eval to correctly interpret the constructed SED_EXPRESSIONS string
eval sed "$SED_EXPRESSIONS" "$INPUT_LOG" > "$OUTPUT_LOG"

if [ $? -eq 0 ]; then
    echo "Log file successfully scrubbed and saved to '$OUTPUT_LOG'."
else
    echo "Error during log scrubbing process."
    exit 1
fi

exit 0
