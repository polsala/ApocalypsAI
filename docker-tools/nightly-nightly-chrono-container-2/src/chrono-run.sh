#!/bin/bash

# This script is the entrypoint for the Chrono-Container.
# It sets the FAKETIME environment variable and then executes the provided command.

# First argument is the command to run.
COMMAND="$1"
shift # Remove the command from arguments

# Second argument (optional) is the temporal anchor (date/time string).
TEMPORAL_ANCHOR="$1"

if [ -z "$COMMAND" ]; then
    echo "Error: No command provided to chrono-run.sh"
    exit 1
fi

if [ -n "$TEMPORAL_ANCHOR" ]; then
    export FAKETIME="$TEMPORAL_ANCHOR"
    echo "Chrono-Container: Anchoring time to $FAKETIME for command: $COMMAND"
    # Preload faketime library and execute the command
    LD_PRELOAD=/usr/lib/faketime/libfaketime.so.1 $COMMAND "$@"
else
    echo "Chrono-Container: Running command without temporal anchor (using container's current time): $COMMAND"
    # Execute the command without faketime
    $COMMAND "$@"
fi
