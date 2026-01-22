#!/bin/bash
set -e

INPUT_FILE=""
OUTPUT_FILE=""

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --input) INPUT_FILE="$2"; shift ;; # Input file path inside the container
        --output) OUTPUT_FILE="$2"; shift ;; # Output file path inside the container
        *) echo "Unknown parameter passed: $1"; exit 1 ;; # Handle unknown arguments
    esac
    shift # Move to the next argument or value
done

# Validate required arguments
if [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: ./entrypoint.sh --input <input_file> --output <output_file>"
    exit 1
fi

# Execute the Python scrubber script
python /app/scrubber.py --input "$INPUT_FILE" --output "$OUTPUT_FILE"
