#!/bin/bash

# Get CPU usage (Linux only)
cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* .*/\1/" | awk '{print int($1+0.5)}')

# Get memory usage
mem_usage=$(free | grep Mem | awk '{print int($3/$2 * 100)}')

# Get disk usage (root)
disk_usage=$(df / | tail -1 | awk '{print int($5/1024)}')

# Get CPU temp (Linux only)
temp=$(sensors | grep 'Package id 0' | awk '{print int($4)}' 2>/dev/null || echo 0)

# Emoji logic
case $cpu_usage in
  [9-99]) cpu="🧠🔥" ;;
  [5-89]) cpu="🧠😅" ;;
  *) cpu="🧠😌" ;;
esac

case $mem_usage in
  [9-99]) mem="MemoryWarning=" ;;
  [5-89]) mem="MemoryWarning=" ;;
  *) mem="MemoryWarning=" ;;
esac

case $disk_usage in
  [9-99]) disk="💾⚠️" ;;
  [5-89]) disk="💾🤔" ;;
  *) disk="💾✅" ;;
esac

case $temp in
  [8-9][0-9]) temp="🔥$temp°C" ;;
  [7-7][0-9]) temp="☀️$temp°C" ;;
  [0-6][0-9]) temp="🧊$temp°C" ;;
  *) temp="❓N/A" ;;
esac

# Output formatted string
echo "${cpu} ${mem}% | ${disk}% | ${temp}"
