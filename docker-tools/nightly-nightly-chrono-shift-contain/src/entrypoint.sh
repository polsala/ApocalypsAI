#!/bin/bash
set -e

# If FAKETIME is set, configure libfaketime
if [ -n "$FAKETIME" ]; then
  export LD_PRELOAD=/usr/lib/faketime/libfaketime.so.1
  export FAKETIME_NO_CACHE=1 # Ensure faketime is applied consistently
  echo "Chrono-Shift activated: FAKETIME=$FAKETIME"
fi

# Execute the command passed to the container
exec "$@"
