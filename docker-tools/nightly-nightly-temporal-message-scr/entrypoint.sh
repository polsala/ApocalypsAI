#!/bin/bash

# This script acts as the entrypoint for the Docker container.
# It parses command-line arguments and passes them to the Python scrambler script.

# Default values
DELAY=0.5
CHAR_SCRAMBLE_LEVEL=1
WORD_REORDER_LEVEL=0
SEED=""
MESSAGE=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --delay)
            DELAY="$2"
            shift
            ;;
        --char-scramble-level)
            CHAR_SCRAMBLE_LEVEL="$2"
            shift
            ;;
        --word-reorder-level)
            WORD_REORDER_LEVEL="$2"
            shift
            ;;
        --seed)
            SEED="$2"
            shift
            ;;
        -h|--help)
            echo "Usage: docker run temporal-scrambler [OPTIONS] <MESSAGE>"
            echo ""
            echo "Options:"
            echo "  --delay <seconds>          Delay in seconds before processing (default: 0.5)"
            echo "  --char-scramble-level <level> Level of character scrambling (0-2, default: 1)"
            echo "  --word-reorder-level <level> Level of word reordering (0-1, default: 0)"
            echo "  --seed <integer>           Seed for random number generator (for deterministic tests)"
            echo "  -h, --help                 Show this help message"
            exit 0
            ;;
        *)
            # Assume the first non-option argument is the message
            if [[ -z "$MESSAGE" ]]; then
                MESSAGE="$1"
            else
                echo "Unknown option or multiple messages: $1"
                exit 1
            fi
            ;;
    esac
    shift
done

if [[ -z "$MESSAGE" ]]; then
    echo "Error: No message provided."
    echo "Usage: docker run temporal-scrambler [OPTIONS] <MESSAGE>"
    exit 1
fi

# Construct the command to run the Python script
PYTHON_CMD="python3 /app/src/scrambler.py \"$MESSAGE\" --delay $DELAY --char-scramble-level $CHAR_SCRAMBLE_LEVEL --word-reorder-level $WORD_REORDER_LEVEL"

if [[ -n "$SEED" ]]; then
    PYTHON_CMD="$PYTHON_CMD --seed $SEED"
fi

# Execute the Python script
eval "$PYTHON_CMD"
