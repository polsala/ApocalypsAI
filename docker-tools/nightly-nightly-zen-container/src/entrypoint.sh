#!/bin/bash

echo "Welcome to the Nightly Zen Container!"
echo "Your minimalist sanctuary for focused development."

if [ "$ZEN_MODE" = "true" ]; then
    echo "Activating Zen Mode..."
    # Run zen_mode.sh in the background, redirecting its output to stdout
    /usr/local/bin/zen_mode.sh &
    ZEN_PID=$!
    echo "Zen Mode PID: $ZEN_PID"
fi

echo "Starting your shell..."
exec bash
