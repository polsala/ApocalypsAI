#!/bin/bash

# Whimsical welcome message
echo "----------------------------------------------------"
echo "Welcome to the ApocalypsAI CLI Survival Toolbox!"
echo "May your commands be swift and your resources plentiful."
echo "----------------------------------------------------"
echo ""

# Set a custom prompt
export PS1="\[\033[01;31m\](ApocalypseKit)\[\033[00m\]:\w\$ "

# Execute the command passed to the container, or default to bash
exec "$@"
