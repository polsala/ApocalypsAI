#!/bin/bash

# Nightly Bash Uptime Emoji
# A whimsical utility to display system uptime with animated emojis

set -euo pipefail

# Configuration
SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default values
DEFAULT_EMOJI="🤖"
VERBOSE=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
  local color="$1"
  local message="$2"
  echo -e "${color}${message}${NC}"
}

# Function to show usage
usage() {
  cat << EOF
Usage: $SCRIPT_NAME [OPTIONS]

Display system uptime with animated emojis and ASCII art.

OPTIONS:
  -e, --emoji EMOJI    Use custom emoji (default: $DEFAULT_EMOJI)
  -v, --verbose        Enable verbose output
  -h, --help          Show this help message

EXAMPLES:
  $SCRIPT_NAME
  $SCRIPT_NAME --emoji "🚀"
  $SCRIPT_NAME --verbose

EOF
}

# Function to get system uptime in seconds
get_uptime_seconds() {
  if command -v uptime >/dev/null 2>&1; then
    # Try to get uptime in seconds directly
    if uptime -s >/dev/null 2>&1; then
      # Linux with uptime -s
      local boot_time
      boot_time=$(uptime -s)
      date -d "$boot_time" +%s
    else
      # Try other methods
      if [[ -f /proc/uptime ]]; then
        # Linux /proc/uptime
        awk '{print int($1)}' /proc/uptime
      elif [[ $(uname -s) == "Darwin" ]]; then
        # macOS
        sysctl -n kern.boottime | awk -F'[=,]' '{print $2}'
      else
        # Fallback: parse uptime command output
        uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}' | awk '{
          if ($0 ~ /day/) {
            days = $1
            hours = $3
            minutes = $5
            print int(days*86400 + hours*3600 + minutes*60)
          } else if ($0 ~ /min/) {
            minutes = $1
            print int(minutes*60)
          } else {
            hours = $1
            minutes = $3
            print int(hours*3600 + minutes*60)
          }
        }'
      fi
    fi
  else
    print_color "$RED" "Error: uptime command not found"
    exit 1
  fi
}

# Function to format uptime
format_uptime() {
  local uptime_seconds=$1
  
  local days=$((uptime_seconds / 86400))
  local hours=$(((uptime_seconds % 86400) / 3600))
  local minutes=$(((uptime_seconds % 3600) / 60))
  
  if [[ $days -gt 0 ]]; then
    echo "${days} day(s), ${hours} hour(s), ${minutes} minute(s)"
  elif [[ $hours -gt 0 ]]; then
    echo "${hours} hour(s), ${minutes} minute(s)"
  else
    echo "${minutes} minute(s)"
  fi
}

# Function to select emoji based on uptime
select_emoji() {
  local uptime_seconds=$1
  local custom_emoji="$2"
  
  # Use custom emoji if provided
  if [[ -n "$custom_emoji" ]]; then
    echo "$custom_emoji"
    return
  fi
  
  # Select emoji based on uptime
  if [[ $uptime_seconds -lt 300 ]]; then
    echo "😴" # Sleeping (less than 5 minutes)
  elif [[ $uptime_seconds -lt 1800 ]]; then
    echo "🚀" # Rocket (less than 30 minutes)
  elif [[ $uptime_seconds -lt 3600 ]]; then
    echo "⚡" # Lightning (less than 1 hour)
  elif [[ $uptime_seconds -lt 21600 ]]; then
    echo "💪" # Flexing (less than 6 hours)
  elif [[ $uptime_seconds -lt 86400 ]]; then
    echo "🔥" # Fire (less than 24 hours)
  elif [[ $uptime_seconds -lt 604800 ]]; then
    echo "🤖" # Robot (less than 1 week)
  elif [[ $uptime_seconds -lt 2592000 ]]; then
    echo "👑" # Crown (less than 1 month)
  else
    echo "🧙" # Wizard (more than 1 month)
  fi
}

# Function to draw ASCII art based on uptime
draw_ascii_art() {
  local uptime_seconds=$1
  
  if [[ $uptime_seconds -lt 3600 ]]; then
    cat << 'EOF'
  __  __
 (  \/  )
  \    /
   \__/
EOF
  elif [[ $uptime_seconds -lt 86400 ]]; then
    cat << 'EOF'
    ___
   /   \
  | () () |
   \  ^  /
    |||||
    |||||
EOF
  elif [[ $uptime_seconds -lt 604800 ]]; then
    cat << 'EOF'
      .-.
     (   )
    (     ) 
     `-.='
      /|\\
     /_|_\\
    /_| |_\\
EOF
  else
    cat << 'EOF'
        .-.
       (   )
      (       )
       `-.=-'
      .-"""""-.
     /          \
    |            |
     \          /
      '-......-'
EOF
  fi
}

# Function to check system health
check_health() {
  local uptime_seconds=$1
  
  if [[ $uptime_seconds -lt 60 ]]; then
    print_color "$RED" "⚠️  System just booted up!"
  elif [[ $uptime_seconds -gt 2592000 ]]; then
    print_color "$YELLOW" "💡 Tip: Consider rebooting for updates!"
  else
    print_color "$GREEN" "✅ System health looks good!"
  fi
}

# Function to validate emoji
validate_emoji() {
  local emoji="$1"
  
  # Basic validation: check if emoji is not empty and not too long
  if [[ -z "$emoji" ]]; then
    print_color "$RED" "Error: Emoji cannot be empty"
    return 1
  fi
  
  if [[ ${#emoji} -gt 10 ]]; then
    print_color "$RED" "Error: Emoji too long"
    return 1
  fi
  
  return 0
}

# Function to run health check
run_health_check() {
  print_color "$BLUE" "=== Health Check ==="
  
  # Check if uptime command exists
  if ! command -v uptime >/dev/null 2>&1; then
    print_color "$RED" "❌ uptime command not found"
    return 1
  fi
  
  # Check if awk exists
  if ! command -v awk >/dev/null 2>&1; then
    print_color "$RED" "❌ awk command not found"
    return 1
  fi
  
  # Check if sed exists
  if ! command -v sed >/dev/null 2>&1; then
    print_color "$RED" "❌ sed command not found"
    return 1
  fi
  
  print_color "$GREEN" "✅ All dependencies found"
  return 0
}

# Function to display verbose information
show_verbose_info() {
  local uptime_seconds=$1
  
  print_color "$BLUE" "=== Verbose Information ==="
  print_color "$BLUE" "Uptime (seconds): $uptime_seconds"
  print_color "$BLUE" "Current time: $(date)"
  print_color "$BLUE" "Hostname: $(hostname)"
  print_color "$BLUE" "OS: $(uname -s)"
  print_color "$BLUE" "Architecture: $(uname -m)"
}

# Main function
main() {
  local custom_emoji=""
  
  # Parse command line arguments
  while [[ $# -gt 0 ]]; do
    case $1 in
      -e|--emoji)
        custom_emoji="$2"
        shift 2
        ;;
      -v|--verbose)
        VERBOSE=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        print_color "$RED" "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
  done
  
  # Run health check
  if ! run_health_check; then
    exit 1
  fi
  
  # Get uptime
  local uptime_seconds
  uptime_seconds=$(get_uptime_seconds)
  
  # Validate uptime
  if ! [[ "$uptime_seconds" =~ ^[0-9]+$ ]]; then
    print_color "$RED" "Error: Could not determine uptime"
    exit 1
  fi
  
  # Validate custom emoji if provided
  if [[ -n "$custom_emoji" ]]; then
    if ! validate_emoji "$custom_emoji"; then
      exit 1
    fi
  fi
  
  # Format uptime
  local formatted_uptime
  formatted_uptime=$(format_uptime "$uptime_seconds")
  
  # Select emoji
  local emoji
  emoji=$(select_emoji "$uptime_seconds" "$custom_emoji")
  
  # Display results
  echo
  print_color "$GREEN" "=== System Uptime ==="
  print_color "$BLUE" "Uptime: $formatted_uptime"
  print_color "$BLUE" "Emoji: $emoji"
  echo
  
  # Display ASCII art
  print_color "$GREEN" "=== ASCII Art ==="
  draw_ascii_art "$uptime_seconds"
  echo
  
  # Show verbose info if requested
  if [[ "$VERBOSE" == "true" ]]; then
    show_verbose_info "$uptime_seconds"
    echo
  fi
  
  # Check system health
  check_health "$uptime_seconds"
  echo
}

# Run main function with all arguments
main "$@"
