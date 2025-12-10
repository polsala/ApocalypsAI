#!/bin/bash

# Get CPU usage percentage (Linux only)
CPU_USAGE=$(top -b -n1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

# Get memory usage percentage
MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2)*100}' | cut -d"." -f1)

# Emoji mapper
get_emoji() {
  local percent=$1
  if (( $(echo "$percent < 30" | bc -l) )); then
    echo "😊"
  elif (( $(echo "$percent < 70" | bc -l) )); then
    echo "😐"
  else
    echo "😟"
  fi
}

# Output result
CPU_EMOJI=$(get_emoji $CPU_USAGE)
MEM_EMOJI=$(get_emoji $MEM_USAGE)

echo "CPU: $CPU_EMOJI | MEM: $MEM_EMOJI"
