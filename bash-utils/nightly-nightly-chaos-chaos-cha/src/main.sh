#!/bin/bash

# Nightly Chaos Chaos Cha
# A whimsical utility for injecting controlled chaos into your workflow

set -euo pipefail

# Configuration
DEFAULT_CHAOS_LEVEL=5
MAX_CHAOS_LEVEL=10
MIN_CHAOS_LEVEL=1

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
CHAOS_LEVEL=$DEFAULT_CHAOS_LEVEL
QUIET_MODE=false

# Array of cryptic messages
CRYPTIC_MESSAGES=(
  "Warning: Quantum fluctuations detected in the build pipeline"
  "Alert: Schrödinger's compiler is both successful and failed"
  "Notice: The build gnomes are performing their sacred rituals"
  "Info: Temporal anomalies may affect deployment timing"
  "Debug: The chaos gremlins are optimizing your code"
  "Error: Reality check failed - proceeding anyway"
  "Critical: Butterflies detected in the dependency graph"
  "Fatal: The build matrix has achieved sentience"
  "Trace: Multiverse alignment in progress"
  "Info: Deploying via quantum tunneling"
)

# Array of harmless surprises
HARMLESS_SURPRISES=(
  "Found 42 hidden TODOs in your code"
  "Discovered a secret backdoor to the build server"
  "Detected unauthorized use of semicolons"
  "Your code has been blessed by the coding monks"
  "Build artifacts have been sprinkled with magic dust"
  "The CI/CD pipeline is now running on hamster wheels"
  "Your git history has been rewritten by time travelers"
  "Deploying with extra sparkle effects"
  "Code review bypassed by ninja developers"
  "Your tests are now running in a parallel universe"
)

# Function to print colored output
print_chaos() {
  local color=$1
  local message=$2
  if [[ $QUIET_MODE == false ]]; then
    echo -e "${color}[CHAOS]${NC} $message"
  fi
}

# Function to get random message
get_random_message() {
  local array=($@)
  local random_index=$((RANDOM % ${#array[@]}))
  echo "${array[$random_index]}"
}

# Function to inject random delays
inject_delay() {
  local max_delay=$((CHAOS_LEVEL * 2))
  local delay=$((RANDOM % max_delay + 1))
  
  if [[ $delay -gt 5 ]]; then
    print_chaos $YELLOW "Injecting $delay second delay due to temporal turbulence"
  fi
  
  sleep $delay
}

# Function to spew cryptic messages
spew_cryptic_messages() {
  local message_count=$((CHAOS_LEVEL / 2 + 1))
  
  for ((i=1; i<=message_count; i++)); do
    local random_message=$(get_random_message "${CRYPTIC_MESSAGES[@]}")
    print_chaos $RED "$random_message"
  done
}

# Function to add harmless surprises
add_harmless_surprises() {
  if [[ $((RANDOM % 3)) -eq 0 ]]; then
    local surprise=$(get_random_message "${HARMLESS_SURPRISES[@]}")
    print_chaos $GREEN "$surprise"
  fi
}

# Function to randomly change terminal settings
chaos_terminal() {
  if [[ $((RANDOM % 5)) -eq 0 ]]; then
    print_chaos $BLUE "Activating terminal chaos mode"
    # Randomly change cursor visibility
    if [[ $((RANDOM % 2)) -eq 0 ]]; then
      tput civis
      sleep 1
      tput cnorm
    fi
  fi
}

# Function to create fake files
create_fake_files() {
  if [[ $((RANDOM % 4)) -eq 0 ]]; then
    local fake_file="/tmp/chaos_$(date +%s)_$(RANDOM).tmp"
    echo "# This file was created by chaos" > "$fake_file"
    print_chaos $YELLOW "Created fake file: $fake_file"
    # Clean up after 10 seconds
    (sleep 10 && rm -f "$fake_file" 2>/dev/null) &
  fi
}

# Function to display usage
usage() {
  cat << EOF
Usage: $0 [OPTIONS]

A whimsical utility for injecting controlled chaos into your workflow.

OPTIONS:
  -c, --chaos-level LEVEL  Set chaos level (1-10, default: 5)
  -q, --quiet             Enable quiet mode (less output)
  -h, --help              Show this help message

EXAMPLES:
  $0                      Run with default chaos level
  $0 -c 9                 Run with high chaos level
  $0 --quiet              Run with minimal output
  $0 -c 3 --quiet         Run with low chaos level and quiet mode

EOF
}

# Function to parse command line arguments
parse_args() {
  while [[ $# -gt 0 ]]; do
    case $1 in
      -c|--chaos-level)
        if [[ -n ${2:-} && $2 != -* ]]; then
          CHAOS_LEVEL=$2
          shift 2
        else
          echo "Error: --chaos-level requires a value"
          exit 1
        fi
        ;;
      -q|--quiet)
        QUIET_MODE=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
  done
  
  # Validate chaos level
  if [[ ! $CHAOS_LEVEL =~ ^[0-9]+$ ]] || [[ $CHAOS_LEVEL -lt $MIN_CHAOS_LEVEL ]] || [[ $CHAOS_LEVEL -gt $MAX_CHAOS_LEVEL ]]; then
    echo "Error: Chaos level must be a number between $MIN_CHAOS_LEVEL and $MAX_CHAOS_LEVEL"
    exit 1
  fi
}

# Function to run chaos sequence
run_chaos() {
  print_chaos $BLUE "Initializing chaos sequence..."
  
  # Inject delays
  inject_delay
  
  # Spew cryptic messages
  spew_cryptic_messages
  
  # Add harmless surprises
  add_harmless_surprises
  
  # Terminal chaos
  chaos_terminal
  
  # Create fake files
  create_fake_files
  
  print_chaos $GREEN "Chaos sequence completed successfully (probably)"
}

# Function to cleanup on exit
cleanup() {
  if [[ $QUIET_MODE == false ]]; then
    echo -e "${BLUE}[CHAOS]${NC} Cleaning up chaos artifacts..."
  fi
  tput cnorm 2>/dev/null || true
}

# Set trap for cleanup
trap cleanup EXIT

# Main execution
main() {
  parse_args "$@"
  run_chaos
}

# Run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
