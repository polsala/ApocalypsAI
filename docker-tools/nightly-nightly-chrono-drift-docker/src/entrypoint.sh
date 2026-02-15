#!/bin/bash
set -euo pipefail

# The first argument is the FAKE_TIME_SPEC
FAKE_TIME_SPEC="$1"
shift

# The rest of the arguments form the COMMAND
COMMAND="$@"

if [ -z "$FAKE_TIME_SPEC" ] || [ -z "$COMMAND" ]; then
    echo "Usage: docker run <image> <FAKE_TIME_SPEC> <COMMAND>"
    echo ""
    echo "FAKE_TIME_SPEC: Absolute (YYYY-MM-DD HH:MM:SS) or relative (+1y, -3w, +5h, etc.) or combined (YYYY-MM-DD HH:MM:SS +1h)"
    echo "COMMAND: The command to execute (e.g., 'date', 'python /app/script.py')"
    exit 1
fi

# Determine the faketime library path. This might vary slightly between systems.
# We'll try a common path for Debian-based systems.
FAKETIME_LIB="/usr/lib/x86_64-linux-gnu/faketime/libfaketime.so.1"

if [ ! -f "$FAKETIME_LIB" ]; then
    echo "Error: faketime library not found at $FAKETIME_LIB" >&2
    echo "Please ensure faketime is correctly installed and the path is correct." >&2
    exit 1
fi

# Set environment variables for faketime
export LD_PRELOAD="$FAKETIME_LIB"
# FAKETIME_NO_CACHE=1 ensures that time doesn't advance within the container
# FAKETIME_UPDATE_INTERVAL=1 would make it advance, but for testing specific points, NO_CACHE is better.
export FAKETIME_NO_CACHE=1

echo "--- Chrono-Drift Initiated ---"
echo "Simulating time: $FAKE_TIME_SPEC"
echo "Executing command: $COMMAND"
echo "------------------------------"

# Execute the command with faketime
# The '--' separates faketime options from the command to execute
exec faketime -f "$FAKE_TIME_SPEC" -- "$COMMAND"
