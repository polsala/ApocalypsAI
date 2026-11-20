#!/bin/bash

# This is the entrypoint for the Docker container.
# It simply executes the main echo-cli script with all arguments.

exec /usr/local/bin/echo-cli "$@"
