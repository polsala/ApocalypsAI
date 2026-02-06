#!/bin/bash

# This script simulates the QuibbleScript interpreter.
# It processes .quib files, looking for the 'QUBBLE' command.

if [ -z "$1" ]; then
    echo "Usage: quibble.sh <quibble_file.quib>"
    echo "       --help : Display this help message."
    exit 1
fi

if [ "$1" == "--help" ]; then
    echo "QuibbleScript Interpreter (simulated)"
    echo "Usage: quibble.sh <quibble_file.quib>"
    echo "Reads a .quib file and executes QUBBLE commands."
    exit 0
fi

QUIBBLE_FILE="$1"

if [ ! -f "$QUIBBLE_FILE" ]; then
    echo "Error: QuibbleScript file '$QUIBBLE_FILE' not found." >&2
    exit 1
fi

while IFS= read -r line; do
    # Trim leading/trailing whitespace
    trimmed_line=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

    # Check if the line starts with 'QUBBLE '
    if [[ "$trimmed_line" =~ ^QUBBLE[[:space:]] ]]; then
        # Extract the string after 'QUBBLE '
        message=$(echo "$trimmed_line" | sed -E 's/^QUBBLE[[:space:]]*(.*)/\1/')
        echo "$message"
    fi
done < "$QUIBBLE_FILE"

exit 0
